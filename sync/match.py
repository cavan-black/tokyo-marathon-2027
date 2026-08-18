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

# Bar a day-shifted CROSS-TRAINING make-up has to clear before it covers a missed run
# (e.g. Sunday's long run walked on Monday's rest day with a loaded pack). Same-day
# substitution needs no size test — being logged on the day is evidence enough that it
# was the session — but a make-up on a *different* day is a claim about a day that
# otherwise reads "Missed", so it has to look like a real session: this many minutes
# total, and at least this share of the missed session's time on feet. Without a bar a
# 15-minute stroll on a rest day would silently retire a 20 km long run.
MIN_SHIFTED_SUB_MINUTES = 30
MIN_SHIFTED_SUB_TIME_RATIO = 0.5
# Coarse min/km used only to turn a session's target km into "roughly this long on
# foot" for the test above. Deliberately a mid-field easy pace rather than any one
# runner's, since it's a threshold, not a number anyone sees.
EASY_PACE_MIN_KM = 5.5


def _reconcile_replacements(all_days, today_iso):
    """Detect a missed session that actually got run on a different (rest) day nearby —
    e.g. Sunday's long run missed, then run on Monday's rest day instead. Deliberately a
    global date-window search rather than per-plan-week: a Sun->Mon swap, the single most
    common real case, always crosses the Mon-Sun week boundary the plan is built around.
    Only matches rest days absorbing real running km against a missed non-rest day with a
    similarly-sized target, within REPLACEMENT_WINDOW_DAYS either direction, preferring
    the closest date and then the closest km match. Mutates all_days (a date-sorted list)
    in place.

    Only sessions strictly BEFORE today can be claimed. Today's own session reads "Missed"
    until something is logged against it, so without this guard a make-up run gets credited
    to a session that hasn't had its chance yet — and on a tie (yesterday's rest day sits
    one day from both Sunday's long run and today's quality) the km match alone decides it,
    which is how Sunday's long run ends up still marked missed."""
    missed = [dd for dd in all_days if dd["type"] != "rest" and dd["status"] == "Missed"
              and dd["target_km"] > 0 and dd["date"] < today_iso]
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


def _cardio_cross(day):
    """The cross-training logged on a day that's actually eligible to stand in for a run."""
    return [c for c in day.get("cross_activities") or [] if c.get("counts_as_substitute", True)]


def _cross_minutes(acts):
    return sum((a.get("moving_time_s") or 0) for a in acts) / 60.0


def _reconcile_shifted_substitutions(all_days, today_iso):
    """Detect a missed session covered by CROSS-TRAINING done on a nearby rest day — e.g.
    Sunday's long run missed, then walked on Monday's rest day with a heavy pack.

    Same shape as _reconcile_replacements, but the make-up isn't a run, so the outcome is
    "Substituted", not "Replaced": the km never join actual_km/ACWR (walking is not
    running load, however loaded the bag), they only come off the week's runnable
    denominator via substituted_km — exactly like a same-day substitution.

    ALL eligible activities on the covering day are aggregated, not just the longest: a
    rucking or walking day is normally logged as several separate activities, and judging
    it on one of them would throw away most of the effort. Only days strictly in the past
    can be covered — a session that hasn't had its chance yet is "Upcoming", not something
    yesterday's walk retroactively retires. Mutates all_days (a date-sorted list) in place."""
    missed = [dd for dd in all_days
              if dd["type"] != "rest" and dd["status"] == "Missed"
              and dd["target_km"] > 0 and dd["date"] < today_iso]
    if not missed:
        return
    # Only an otherwise-empty rest day donates: cross-training on a run day is already
    # resolved same-day, and a rest day that hosted a real run is _reconcile_replacements'
    # case and has been claimed by it already (this runs second, so runs win).
    donors = []
    for dd in all_days:
        if dd["type"] != "rest" or dd["actual_km"] > 0.05 or dd.get("replaces"):
            continue
        acts = _cardio_cross(dd)
        minutes = _cross_minutes(acts)
        if acts and minutes >= MIN_SHIFTED_SUB_MINUTES:
            donors.append((dd, acts, minutes))

    used = set()
    for dd, acts, minutes in donors:
        dd_date = date.fromisoformat(dd["date"])
        candidates = []
        for md in missed:
            if md["date"] in used:
                continue
            gap = abs((date.fromisoformat(md["date"]) - dd_date).days)
            if gap > REPLACEMENT_WINDOW_DAYS:
                continue
            est_minutes = md["target_km"] * EASY_PACE_MIN_KM
            if minutes < MIN_SHIFTED_SUB_TIME_RATIO * est_minutes:
                continue
            candidates.append((gap, abs(minutes - est_minutes), md))
        if not candidates:
            continue
        # closest date first, then the session this effort most closely resembles in time
        _, _, best = min(candidates, key=lambda c: (c[0], c[1]))
        used.add(best["date"])
        lead = max(acts, key=lambda a: a.get("moving_time_s") or 0)
        best["status"] = "Substituted"
        best["substituted_by"] = {
            "date": dd["date"], "dow": dd["dow"], "count": len(acts),
            "activity_type": lead.get("activity_type"), "name": lead.get("name"),
            "manual": any(a.get("manual") for a in acts),
            "moving_time_s": int(round(minutes * 60)),
            "distance_km": round(sum(a.get("distance_km") or 0 for a in acts), 2),
        }
        dd["substitutes"] = {"date": best["date"], "dow": best["dow"], "session": best["session"],
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
    calendar day.

    Cross-training make-ups shift too: a missed session covered by cardio cross-training
    on a nearby rest day (Sunday's long run walked on Monday) is "Substituted" with the
    covering day recorded in substituted_by — see _reconcile_shifted_substitutions."""
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
            # Only CARDIO cross-training can stand in for a run (football yes, gym no —
            # see strava.CARDIO_CROSS_TYPES). Non-cardio activities still ride along in
            # cross_activities for display, they just never resolve the day.
            sub_acts = [c for c in cross_acts if c.get("counts_as_substitute", True)]
            if d["type"] != "rest" and actual_km <= 0.05 and sub_acts:
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
    # runs first: a real make-up run always beats a cross-training one for the same day
    _reconcile_replacements(all_days, today_iso)
    _reconcile_shifted_substitutions(all_days, today_iso)

    # Pass 2: regroup by week and aggregate.
    by_week = defaultdict(list)
    for dd in all_days:
        by_week[dd["week"]].append(dd)

    days = {}
    weeks = {}
    for wk in plan["weeks"]:
        pk = ak = pk_due = done = partial = missed = substituted = replaced = quality_hit = quality_planned = 0
        sub_km = 0  # target km of days covered by cross-training — never runnable, see below
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
            elif status == "Substituted": done += 1; substituted += 1; sub_km += dd["target_km"]
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
        # read as "under-target" just because the week isn't finished yet. Substituted
        # km come off the denominator too: those km were deliberately covered by
        # cross-training and are never going to appear as running load, so counting
        # them would flag an honoured week as under-target.
        due_runnable = max(pk_due - sub_km, 0)
        if due_runnable > 0 and ak < 0.70 * due_runnable:
            flag = "⚠ Under-target — consider holding volume / repeating the week"
        elif quality_planned and (quality_planned - quality_hit) >= 2:
            flag = "⚠ ≥2 quality sessions missed — prioritise them next week"
        elif due_runnable > 0 and ak > 1.15 * due_runnable:
            flag = "⚠ Over-target — watch fatigue/injury; don't overcook"
        else:
            flag = "✓ On track"
        weeks[str(wk["week"])] = {
            "planned_km": round(pk, 1), "planned_km_due": round(pk_due, 1), "actual_km": round(ak, 1),
            # km that were planned but got covered by cross-training, so they can never
            # show up as running km. Anything judging volume-hit (e.g. the dashboard's
            # "Crushed" chip) must measure against planned_km MINUS this, otherwise a week
            # containing a substitution is mathematically incapable of hitting target.
            "substituted_km": round(sub_km, 1),
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
