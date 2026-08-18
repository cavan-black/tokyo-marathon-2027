"""Hand-entered sessions that never reached Strava.

Some sessions genuinely have no device behind them — a BJJ class, a pickup game, a swim
on a dead watch. With everything derived from Strava those days read "Missed", which is
worse than merely wrong: it under-reports consistency and pushes the coach rule toward
"hold volume / repeat the week" on a week that was actually honoured.

Entries live in data/manual_<runner>.json and are merged into the CROSS-TRAINING stream
only, never the running stream. Hand-entered km would flow straight into actual_km and
ACWR, and a training-load signal you can type into is not a signal — the whole point of
ACWR is that it's measured. So a manual entry can satisfy a day (giving it "Substituted"
exactly like a synced football session would) but can never add running load, and every
record it produces carries manual=True so the dashboard can say where the number came
from rather than passing it off as measured.

Format — a JSON list, each entry needing at least date, activity_type and moving_time_s:

    [
      {"date": "2026-08-18", "activity_type": "MartialArts",
       "name": "BJJ sparring", "moving_time_s": 10800, "note": "3 h, no device"}
    ]

activity_type must be one of sync/strava.py's CROSS_TYPES; whether it can stand in for a
run follows the same CARDIO_CROSS_TYPES rule that synced activities obey, so writing an
entry by hand grants no privilege a recorded one wouldn't have had.
"""
import json
import os
from datetime import date

from sync.strava import CARDIO_CROSS_TYPES, CROSS_TYPES

REQUIRED = ("date", "activity_type", "moving_time_s")


def _normalise(entry, runner_id, i):
    where = f"manual_{runner_id}.json[{i}]"
    for k in REQUIRED:
        if entry.get(k) in (None, ""):
            raise ValueError(f"{where}: missing required field {k!r}")
    typ = entry["activity_type"]
    if typ not in CROSS_TYPES:
        raise ValueError(f"{where}: unknown activity_type {typ!r} — "
                         f"expected one of {', '.join(sorted(CROSS_TYPES))}")
    try:
        date.fromisoformat(entry["date"])
    except ValueError:
        raise ValueError(f"{where}: date {entry['date']!r} is not YYYY-MM-DD") from None
    secs = int(entry["moving_time_s"])
    if secs <= 0:
        raise ValueError(f"{where}: moving_time_s must be positive, got {secs}")
    return {
        "id": entry.get("id") or f"manual-{runner_id}-{entry['date']}-{i}",
        "date": entry["date"],
        "name": entry.get("name") or typ,
        "activity_type": typ,
        # deliberately fixed at zero — see module docstring
        "distance_km": 0.0,
        "moving_time_s": secs,
        "pace_min_km": None,
        "avg_hr": entry.get("avg_hr"),
        "max_hr": None,
        "elev_gain_m": None,
        "route": [],
        "counts_as_substitute": typ in CARDIO_CROSS_TYPES,
        "manual": True,
    }


def load(data_dir, runner_id, synced=()):
    """Return this runner's hand-entered cross-training, in simplify_cross's shape.

    synced: the cross-training already pulled from Strava. An entry is dropped when that
    day already holds a synced activity of the same type — if the session later shows up
    from a device (a watch that synced late, a session added in the Strava app), the
    recorded one wins and the hand-written note stops double-counting the day."""
    path = os.path.join(data_dir, f"manual_{runner_id}.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        raise ValueError(f"manual_{runner_id}.json: expected a JSON list of entries")
    already = {(c.get("date"), c.get("activity_type")) for c in synced}
    out = []
    for i, entry in enumerate(raw):
        rec = _normalise(entry, runner_id, i)
        if (rec["date"], rec["activity_type"]) not in already:
            out.append(rec)
    return out
