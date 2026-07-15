#!/usr/bin/env python3
"""Pull each runner's Strava activities, match to their plan, write data/progress_<id>.json.

Shared app creds:   STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET
Per-runner tokens:  STRAVA_REFRESH_TOKEN_CAV, STRAVA_REFRESH_TOKEN_JAMIE
                    (or STRAVA_REFRESH_TOKEN as a single-runner fallback)
"""
import os, sys, json
from datetime import datetime, timezone

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, ROOT)

from sync import strava, match  # noqa: E402


def load_env():
    envp = os.path.join(ROOT, ".env")
    if os.path.exists(envp):
        for line in open(envp, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def token_for(runner_id):
    return (os.environ.get(f"STRAVA_REFRESH_TOKEN_{runner_id.upper()}")
            or os.environ.get("STRAVA_REFRESH_TOKEN"))


def sync_runner(runner_id, write=True):
    """Sync one runner; returns their progress dict (or None if no creds)."""
    load_env()
    cid = os.environ.get("STRAVA_CLIENT_ID")
    csecret = os.environ.get("STRAVA_CLIENT_SECRET")
    rtoken = token_for(runner_id)
    plan_path = os.path.join(DATA, f"plan_{runner_id}.json")
    if not os.path.exists(plan_path):
        print(f"[{runner_id}] no plan_{runner_id}.json — run plan_generator first."); return None
    plan = json.load(open(plan_path, encoding="utf-8"))
    if not (cid and csecret and rtoken):
        print(f"[{runner_id}] no Strava credentials — leaving progress untouched."); return None

    start = datetime.fromisoformat(plan["meta"]["start"]).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    # never ask Strava for a future window (plan may not have started yet)
    after = min(start.timestamp(), now.timestamp())
    access, new_refresh = strava.refresh_access_token(cid, csecret, rtoken)
    runs = strava.simplify(strava.get_activities(access, after_epoch=after))
    progress = match.match(plan, runs)
    progress["last_sync"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    progress["tracker"] = match.tracker(progress)
    if write:
        with open(os.path.join(DATA, f"progress_{runner_id}.json"), "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)
    if new_refresh != rtoken:
        print(f"[{runner_id}] NOTE: refresh token rotated → update secret to: {new_refresh}")
    logged = sum(1 for d in progress["days"].values() if d["status"] not in ("Rest", "Missed", "Upcoming"))
    print(f"[{runner_id}] {len(runs)} runs · {logged} sessions logged · {progress['last_sync']}")
    return progress


def sync_all(write=True):
    manifest_path = os.path.join(DATA, "runners.json")
    runners = json.load(open(manifest_path, encoding="utf-8")) if os.path.exists(manifest_path) else []
    return {r["id"]: sync_runner(r["id"], write=write) for r in runners}


if __name__ == "__main__":
    sync_all()
