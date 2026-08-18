"""Minimal Strava API client — personal single-user use.
Needs a Strava API app (client id/secret) and a one-time refresh token (see get_token.py)."""
import time
from datetime import datetime, timedelta
import requests

TOKEN_URL = "https://www.strava.com/oauth/token"
ACT_URL   = "https://www.strava.com/api/v3/athlete/activities"


def refresh_access_token(client_id, client_secret, refresh_token):
    """Exchange the long-lived refresh token for a short-lived access token."""
    r = requests.post(TOKEN_URL, data={
        "client_id": client_id, "client_secret": client_secret,
        "grant_type": "refresh_token", "refresh_token": refresh_token,
    }, timeout=30)
    r.raise_for_status()
    j = r.json()
    # Strava may rotate the refresh token — caller should persist the new one if so.
    return j["access_token"], j.get("refresh_token", refresh_token)


def get_activities(access_token, after_epoch=None, before_epoch=None, per_page=100, max_pages=10):
    """Fetch the athlete's activities in a time window. Returns a list of dicts."""
    out, page = [], 1
    headers = {"Authorization": f"Bearer {access_token}"}
    while page <= max_pages:
        params = {"per_page": per_page, "page": page}
        if after_epoch:  params["after"] = int(after_epoch)
        if before_epoch: params["before"] = int(before_epoch)
        r = requests.get(ACT_URL, headers=headers, params=params, timeout=30)
        if r.status_code == 429:  # rate limited — back off and stop politely
            time.sleep(2)
            break
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        out.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return out


def decode_polyline(encoded):
    """Google encoded-polyline decoder (Strava's summary_polyline format)."""
    if not encoded:
        return []
    points, index, lat, lng = [], 0, 0, 0
    n = len(encoded)
    while index < n:
        for is_lat in (True, False):
            shift, result = 0, 0
            while True:
                b = ord(encoded[index]) - 63
                index += 1
                result |= (b & 0x1f) << shift
                shift += 5
                if b < 0x20:
                    break
            d = ~(result >> 1) if (result & 1) else (result >> 1)
            if is_lat:
                lat += d
            else:
                lng += d
        points.append((round(lat / 1e5, 5), round(lng / 1e5, 5)))
    return points


def _privacy_trimmed_route(encoded, frac=0.12, min_drop=5):
    """Decode a route and drop a chunk off BOTH ends so the exact start/finish (often
    home) is never stored — only the middle of the route, which is what we persist."""
    pts = decode_polyline(encoded)
    n = len(pts)
    if n < 20:
        return []  # too short to trim safely and still be meaningfully private — skip it
    drop = max(min_drop, int(n * frac))
    trimmed = pts[drop:n - drop]
    return trimmed if len(trimmed) >= 5 else []


RUN_TYPES = ("Run", "TrailRun", "VirtualRun")
# Cardio cross-training that CAN stand in for a planned run day (e.g. Jamie's football)
# without being counted as running km — see sync/match.py's "Substituted" status. The
# aerobic stimulus is comparable enough that the day counts as satisfied.
CARDIO_CROSS_TYPES = ("Soccer", "Ride", "Swim", "Hike", "Walk", "Rowing", "Elliptical",
                      "StairStepper", "Kayaking", "NordicSki", "BackcountrySki", "Snowboard",
                      # Strava has no martial-arts type, so nothing synced ever arrives as
                      # this — it exists for sync/manual.py, where grappling and sparring
                      # get written down by hand. Kept out of the "Workout" catch-all on
                      # purpose: a named entry is affirmatively cardio, "Workout" isn't.
                      "MartialArts")
# Logged and shown on the day, but NEVER a valid substitute for a run: strength work is a
# different stimulus entirely, and it's already separately scheduled as the S&C session —
# counting it would both excuse a missed run and double-count the gym. "Workout" is
# Strava's generic catch-all bucket, so it can't be affirmatively verified as cardio and
# is treated the same way.
NON_CARDIO_CROSS_TYPES = ("WeightTraining", "Workout", "Crossfit", "Yoga")
CROSS_TYPES = CARDIO_CROSS_TYPES + NON_CARDIO_CROSS_TYPES


EARLY_HOUR_CUTOFF = 4  # activities starting before this hour count as the night before


def _training_date(start_date_local):
    """Which day an activity 'counts' as. A session logged starting in the small hours
    (e.g. 03:00) is almost always a night-before session that crossed midnight — either
    it genuinely ran late, or Strava/the watch uploaded it with a shifted timestamp —
    rather than someone training before 4am. Bucket those onto the previous calendar day."""
    raw = start_date_local or ""
    if not raw:
        return ""
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return raw[:10]
    if dt.hour < EARLY_HOUR_CUTOFF:
        dt -= timedelta(days=1)
    return dt.date().isoformat()


def _simplify_one(a):
    dist_km = (a.get("distance") or 0) / 1000.0
    moving = a.get("moving_time") or 0
    pace = (moving / 60.0) / dist_km if dist_km > 0.3 else None  # min/km
    return {
        "id": a.get("id"),
        "date": _training_date(a.get("start_date_local")),
        "name": a.get("name"),
        "activity_type": a.get("type"),
        "distance_km": round(dist_km, 2),
        "moving_time_s": moving,
        "pace_min_km": round(pace, 3) if pace else None,
        "avg_hr": a.get("average_heartrate"),
        "max_hr": a.get("max_heartrate"),
        "elev_gain_m": a.get("total_elevation_gain"),
        # Privacy: never store the raw start point or full polyline — only a
        # trimmed middle section (start/finish, usually home, is dropped).
        "route": _privacy_trimmed_route((a.get("map") or {}).get("summary_polyline")),
    }


def simplify(activities):
    """Keep only running activities and the fields we need for matching."""
    return [_simplify_one(a) for a in activities if a.get("type") in RUN_TYPES]


def simplify_cross(activities):
    """Non-running activities (football, gym, etc.) — tracked separately so they never
    inflate running km/ACWR. Each carries counts_as_substitute so sync/match.py can tell
    a cardio session that genuinely covers a missed run from a gym session that doesn't."""
    out = []
    for a in activities:
        typ = a.get("type")
        if typ not in CROSS_TYPES:
            continue
        s = _simplify_one(a)
        s["counts_as_substitute"] = typ in CARDIO_CROSS_TYPES
        out.append(s)
    return out
