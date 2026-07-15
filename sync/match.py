"""Match synced Strava runs to planned sessions and build the progress structure."""
from collections import defaultdict
from datetime import date

# pace targets (min/km) used only to annotate quality/long efforts
MP = 4.017          # 4:01/km
THRESHOLD = 3.80    # ~3:48/km


def _fmt_pace(p):
    if not p:
        return None
    m = int(p); s = int(round((p - m) * 60))
    if s == 60:
        m, s = m + 1, 0
    return f"{m}:{s:02d}"


def classify(target_km, actual_km, typ):
    if typ == "rest":
        return "Rest"
    if actual_km <= 0.05:
        return "Missed"
    if target_km <= 0:
        return "Done" if actual_km > 0 else "Rest"
    ratio = actual_km / target_km
    if ratio >= 0.85:
        return "Done"
    if ratio >= 0.5:
        return "Partial"
    return "Missed"


def match(plan, runs):
    """Return a progress dict keyed by date + weekly rollups."""
    by_date = defaultdict(list)
    for r in runs:
        if r["date"]:
            by_date[r["date"]].append(r)

    today_iso = date.today().isoformat()
    days = {}
    weeks = {}
    for wk in plan["weeks"]:
        pk = ak = done = partial = missed = quality_hit = quality_planned = 0
        long_done = None
        for d in wk["days"]:
            acts = by_date.get(d["date"], [])
            actual_km = round(sum(a["distance_km"] for a in acts), 2)
            # session-weighted pace (longest activity that day)
            pace = None
            if acts:
                lead = max(acts, key=lambda a: a["distance_km"])
                pace = lead.get("pace_min_km")
            future = d["date"] > today_iso
            if future and d["type"] != "rest" and actual_km <= 0.05:
                status = "Upcoming"
            else:
                status = classify(d["target_km"], actual_km, d["type"])
            days[d["date"]] = {
                "week": wk["week"], "dow": d["dow"], "type": d["type"],
                "session": d["session"], "target_km": d["target_km"],
                "actual_km": actual_km, "status": status,
                "pace_min_km": pace, "pace_str": _fmt_pace(pace),
                "activities": acts,
            }
            pk += d["target_km"]; ak += actual_km
            if d["type"] == "rest":
                continue
            if status == "Done": done += 1
            elif status == "Partial": partial += 1
            elif status == "Missed": missed += 1
            if d["type"] == "quality":
                quality_planned += 1
                if status == "Done": quality_hit += 1
            if d["type"] in ("long", "race") and d["dow"] == "Sun":
                long_done = (status == "Done")
        # coach-rule flag (suggestion, not auto-change)
        if pk > 0 and ak < 0.70 * pk:
            flag = "⚠ Under-target — consider holding volume / repeating the week"
        elif quality_planned and (quality_planned - quality_hit) >= 2:
            flag = "⚠ ≥2 quality sessions missed — prioritise them next week"
        elif pk > 0 and ak > 1.15 * pk:
            flag = "⚠ Over-target — watch fatigue/injury; don't overcook"
        else:
            flag = "✓ On track"
        weeks[str(wk["week"])] = {
            "planned_km": round(pk, 1), "actual_km": round(ak, 1),
            "done": done, "partial": partial, "missed": missed,
            "quality_hit": quality_hit, "quality_planned": quality_planned,
            "long_done": long_done, "flag": flag,
        }
    return {"days": days, "weeks": weeks}


def tracker(progress):
    """Fitness signal: latest threshold + MP/long paces (goal-agnostic labels)."""
    latest_t = latest_mp = None
    for dt in sorted(progress["days"].keys()):
        d = progress["days"][dt]
        if d["status"] in ("Missed", "Rest", "Upcoming") or not d.get("pace_min_km"):
            continue
        s = d["session"]
        if d["type"] == "quality" and ("Threshold" in s or "Tempo" in s or "@ T" in s or "Cruise" in s):
            latest_t = (dt, d["pace_str"], d["pace_min_km"])
        if d["type"] == "long" or "@ MP" in s or "MP" in s:
            latest_mp = (dt, d["pace_str"], d["pace_min_km"])
    return {"threshold_latest": latest_t, "mp_latest": latest_mp}
