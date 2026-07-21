"""Minimal Strava API client — personal single-user use.
Needs a Strava API app (client id/secret) and a one-time refresh token (see get_token.py)."""
import time
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


def simplify(activities):
    """Keep only running activities and the fields we need for matching."""
    runs = []
    for a in activities:
        if a.get("type") not in ("Run", "TrailRun", "VirtualRun"):
            continue
        dist_km = (a.get("distance") or 0) / 1000.0
        moving = a.get("moving_time") or 0
        pace = (moving / 60.0) / dist_km if dist_km > 0.3 else None  # min/km
        runs.append({
            "id": a.get("id"),
            "date": (a.get("start_date_local") or "")[:10],
            "name": a.get("name"),
            "distance_km": round(dist_km, 2),
            "moving_time_s": moving,
            "pace_min_km": round(pace, 3) if pace else None,
            "avg_hr": a.get("average_heartrate"),
            "max_hr": a.get("max_heartrate"),
            "elev_gain_m": a.get("total_elevation_gain"),
            # Privacy: never store the raw start point or full polyline — only a
            # trimmed middle section (start/finish, usually home, is dropped).
            "route": _privacy_trimmed_route((a.get("map") or {}).get("summary_polyline")),
        })
    return runs
