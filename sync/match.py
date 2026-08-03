"""Match synced Strava runs to planned sessions and build the progress structure."""
from collections import defaultdict
from datetime import date, timedelta

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


REPLACEMENT_WINDOW_DAYS = 3  # how far a missed session's real make-up day can be searched


def _reconcile_replacements(all_days):
    """Detect a missed session that actually got run on a different (rest) day nearby —
    e.g. Sunday's long run missed, then run on Monday's rest day instead. Deliberately a
    global date-window search rather than per-plan-week: a Sun->Mon swap, the single most
    common real case, always crosses the Mon-Sun week boundary the plan is built around.
    Only matches rest days absorbing real running km against a missed non-rest day with a
    similarly-sized target, within REPLACEMENT_WINDOW_DAYS either direction, preferring
    the closest date and then the closest km match. Mutates all_days (a date-sorted list)
    in place."""
    missed = [dd for dd in all_days if dd["type"] != "rest" and dd["status"] == "Missed" and dd["target_km"] > 0]
    surplus = [dd for dd in all_days if dd["type"] == "rest" and dd["actual_km"] > 0.5]
    used = set()
    for sd in surplus:
        sd_date = date.fromisoformat(sd["date"])
        candidates = []
        for md in missed:
            if md["date"] in used:
                continue
            gap = abs((date.fromisoformat(md["date"]) - sd_date).days)
            if gap <= REPLACEMENT_WINDOW_DAYS:
                candidates.append((gap, md))
        if not candidates:
            continue
        # closest date first, then closest km match within that
        min_gap = min(g for g, _ in candidates)
        same_gap = [md for g, md in candidates if g == min_gap]
        best = min(same_gap, key=lambda md: abs(sd["actual_km"] / md["target_km"] - 1.0))
        ratio = sd["actual_km"] / best["target_km"]
        if 0.6 <= ratio <= 1.6:
            used.add(best["date"])
            best["status"] = "Replaced"
            best["replaced_by"] = {"date": sd["date"], "dow": sd["dow"], "actual_km": sd["actual_km"],
                                    "pace_str": sd["pace_str"], "pace_min_km": sd["pace_min_km"]}
            sd["replaces"] = {"date": best["date"], "dow": best["dow"], "session": best["session"],
                               "type": best["type"], "target_km": best["target_km"]}


def match(plan, runs, cross_runs=None):
    """Return a progress dict keyed by date + weekly rollups.

    cross_runs: non-running activities (football, gym, etc. — see strava.simplify_cross)
    that can substitute for a planned run day. They never count toward actual_km/ACWR
    (that stays running-load-only) but a same-day cross activity on a non-rest day with
    no run logged is marked "Substituted" instead of "Missed".

    Also detects same-sport day-shifted runs (e.g. Sunday's long run actually done on
    Monday's rest day) and marks the missed day "Replaced" instead — see
    _reconcile_replacements. Unlike a substitution, the km already counts toward
    actual_km/ACWR as normal since it's a real run, just logged against its own real
    calendar day."""
    by_date = defaultdict(list)
    for r in runs:
        if r["date"]:
            by_date[r["date"]].append(r)
    cross_by_date = defaultdict(list)
    for c in (cross_runs or []):
        if c["date"]:
            cross_by_date[c["date"]].append(c)

    today_iso = date.today().isoformat()

    # Pass 1: match each day to its own calendar date, across the whole plan (not per
    # week) so the replacement search below can look across a week boundary.
    all_days = []
    for wk in plan["weeks"]:
        for d in wk["days"]:
            acts = by_date.get(d["date"], [])
            cross_acts = cross_by_date.get(d["date"], [])
            actual_km = round(sum(a["distance_km"] for a in acts), 2)
            # session-weighted pace (longest activity that day)
            pace = None
            if acts:
                lead = max(acts, key=lambda a: a["distance_km"])
                pace = lead.get("pace_min_km")
            future = d["date"] > today_iso
            if d["type"] != "rest" and actual_km <= 0.05 and cross_acts:
                # a logged cross-training activity always resolves the day, even if the
                # date is nominally "future" relative to today — it already happened.
                status = "Substituted"
            elif future and d["type"] != "rest" and actual_km <= 0.05:
                status = "Upcoming"
            else:
                status = classify(d["target_km"], actual_km, d["type"])
            all_days.append({
                "date": d["date"], "week": wk["week"], "dow": d["dow"], "type": d["type"],
                "session": d["session"], "target_km": d["target_km"], "future": future,
                "actual_km": actual_km, "status": status,
                "pace_min_km": pace, "pace_str": _fmt_pace(pace),
                "activities": acts, "cross_activities": cross_acts,
            })
    _reconcile_replacements(all_days)

    # Pass 2: regroup by week and aggregate.
    by_week = defaultdict(list)
    for dd in all_days:
        by_week[dd["week"]].append(dd)

    days = {}
    weeks = {}
    for wk in plan["weeks"]:
        pk = ak = pk_due = done = partial = missed = substituted = replaced = quality_hit = quality_planned = 0
        long_done = None
        for dd in by_week[wk["week"]]:
            future = dd.pop("future")
            date_key = dd.pop("date")
            days[date_key] = dd
            pk += dd["target_km"]; ak += dd["actual_km"]
            if not future:
                pk_due += dd["target_km"]
            if dd["type"] == "rest":
                continue
            status = dd["status"]
            # a substituted cross-training session (e.g. football) or a same-sport run
            # done on a different day both count toward consistency exactly like "Done"
            # — the day was satisfied, just not with a run logged on its own calendar
            # date, so they're tracked separately purely for display, never as a lesser
            # outcome.
            if status == "Done": done += 1
            elif status == "Substituted": done += 1; substituted += 1
            elif status == "Replaced": done += 1; replaced += 1
            elif status == "Partial": partial += 1
            elif status == "Missed": missed += 1
            if dd["type"] == "quality" and not future:
                quality_planned += 1
                if status in ("Done", "Substituted", "Replaced"): quality_hit += 1
            if dd["type"] in ("long", "race") and dd["dow"] == "Sun":
                long_done = (status in ("Done", "Replaced"))
        # coach-rule flag (suggestion, not auto-change) — judged against km DUE so
        # far this week, not the full week's target, so a Tuesday check-in doesn't
        # read as "under-target" just because the week isn't finished yet.
        if pk_due > 0 and ak < 0.70 * pk_due:
            flag = "⚠ Under-target — consider holding volume / repeating the week"
        elif quality_planned and (quality_planned - quality_hit) >= 2:
            flag = "⚠ ≥2 quality sessions missed — prioritise them next week"
        elif pk_due > 0 and ak > 1.15 * pk_due:
            flag = "⚠ Over-target — watch fatigue/injury; don't overcook"
        else:
            flag = "✓ On track"
        weeks[str(wk["week"])] = {
            "planned_km": round(pk, 1), "planned_km_due": round(pk_due, 1), "actual_km": round(ak, 1),
            "done": done, "partial": partial, "missed": missed,
            "substituted": substituted, "replaced": replaced,
            "quality_hit": quality_hit, "quality_planned": quality_planned,
            "long_done": long_done, "flag": flag,
        }
    return {"days": days, "weeks": weeks}


def tracker(progress):
    """Fitness signal: latest threshold + MP/long paces (goal-agnostic labels)."""
    latest_t = latest_mp = None
    for dt in sorted(progress["days"].keys()):
        d = progress["days"][dt]
        replaces = d.get("replaces")  # a rest day that actually hosted another day's run
        if not replaces and (d["status"] in ("Missed", "Rest", "Upcoming") or not d.get("pace_min_km")):
            continue
        if replaces and not d.get("pace_min_km"):
            continue
        typ = replaces["type"] if replaces else d["type"]
        s = replaces["session"] if replaces else d["session"]
        if typ == "quality" and ("Threshold" in s or "Tempo" in s or "@ T" in s or "Cruise" in s):
            latest_t = (dt, d["pace_str"], d["pace_min_km"])
        if typ == "long" or "@ MP" in s or "MP" in s:
            latest_mp = (dt, d["pace_str"], d["pace_min_km"])
    return {"threshold_latest": latest_t, "mp_latest": latest_mp}
