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
            "start_latlng": a.get("start_latlng") or None,
            "polyline": (a.get("map") or {}).get("summary_polyline") or None,
        })
    return runs
