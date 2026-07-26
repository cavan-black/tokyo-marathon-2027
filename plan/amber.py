"""Amber's half marathon plan as structured data. build() -> plan dict.
28, starting from scratch, no fixed time goal — "best she can". Week 1 includes a
time trial to set a real baseline; pace zones are effort-based until that lands.
19-week build to the Sevilla Half (6 Dec 2026), same race Cav is tuning up at and
Jamie is using as a training run."""
from datetime import date, timedelta
import content as C

ID, NAME, GOAL = "amber", "Amber", "Half marathon — best she can"
START = date(2026, 7, 27)
RACE  = date(2026, 12, 6)

VOL = [12, 15, 18, 16,
       20, 23, 26, 22,
       34, 31, 34, 29,
       37, 40, 43, 36,
       30, 20, 12]
LR  = [4, 6, 8, 7,
       9, 10, 12, 9,
       13, 14, 16, 12,
       17, 18, 19, 14,
       12, 8, 21.0975]

# Long-run weekends with a steady/controlled finish — always alternate with an easy one.
HARD_LR = {7, 11, 13, 15}
CUTBACK = {4, 8, 12, 16}


def phase(w):
    if w <= 4:  return "Getting started"
    if w <= 8:  return "Aerobic base"
    if w <= 12: return "Endurance build"
    if w <= 16: return "Half-specific peak"
    return "Taper & race"


def tue(w):
    if w == 1:
        return "Easy 20 min, conversational — just moving, nothing more", "easy"
    if w <= 4:
        return "Easy 20-25 min + 4 x 20s strides", "easy"
    if w <= 12:
        lib = ["Easy 30 min + strides", "Steady 30 min, negative split", "Easy 30-35 min + strides",
               "Steady 30 min + 4 x 1 min controlled pickups"]
        s = lib[(w - 5) % len(lib)]
        return s, ("quality" if "pickups" in s else "easy")
    if w <= 16:
        lib = ["Tempo: 15 min at a controlled-hard effort, 5 min jog either side", "Easy 35-40 min",
               "Tempo: 2 x 10 min at a controlled-hard effort, 3 min jog between", "Easy 35 min + strides"]
        s = lib[(w - 13) % len(lib)]
        return s, ("quality" if "Tempo" in s else "easy")
    return {17: "Easy 25 min + strides", 18: "Easy 20 min + strides",
            19: "Rest or 10 min shakeout"}[w], "easy"


def wed(w):
    if w <= 4:
        return "Rest, or an easy 20 min walk/swim/bike", "rest"
    return "Easy 20-25 min, truly easy", "easy"


def thu(w):
    if w == 1:
        return "Rest — recover from the time trial", "rest"
    if w <= 4:
        return "Easy 20-25 min", "easy"
    if w <= 16:
        lib = ["Easy 25-30 min", "Easy 30 min", "Steady 30 min, conversational by the end", "Easy 30-35 min"]
        return lib[(w - 5) % len(lib)], "easy"
    return {17: "Easy 20 min", 18: "Rest", 19: "Rest"}[w], ("rest" if w in (18, 19) else "easy")


def sat(w):
    if w == 1:
        return "5K time trial or local parkrun — flat out, this sets your real baseline", "tt", 5
    if w <= 4:
        return None, "easy", None
    if w == 9:
        return "10K time trial or local race (optional check-in)", "tt", 10
    if w in (17, 18):
        return {17: "Easy 20 min + strides", 18: "Easy 15 min"}[w], "easy", None
    if w == 19:
        return "Shakeout 15-20 min + a few strides", "easy", 3
    return None, "easy", None


def sun(w):
    d = LR[w - 1]
    txt = {
        1: "Easy 4 km, whatever's left in the legs after yesterday's time trial",
        4: f"{d:g} km easy — cut-back",
        7: f"{d:g} km, last 3 km at a steady, controlled effort",
        8: f"{d:g} km easy — cut-back",
        11: f"{d:g} km, last 4 km at a steady, controlled effort",
        12: f"{d:g} km easy — cut-back",
        13: f"{d:g} km, last 5 km at a steady, controlled effort",
        15: f"{d:g} km, last 6 km at a steady, controlled effort — biggest test before taper",
        16: f"{d:g} km easy — cut-back",
        19: "RACE DAY — Sevilla Half Marathon · run to how training actually went, not a number picked in July",
    }
    t = txt.get(w, f"{d:g} km easy")
    return t, ("race" if w == 19 else "long")


def build_week(w):
    v = VOL[w - 1]
    lr = LR[w - 1]
    tue_txt, tue_type = tue(w)
    wed_txt, wed_type = wed(w)
    thu_txt, thu_type = thu(w)
    sun_txt, sun_type = sun(w)
    sat_txt, sat_type, sat_fixed = sat(w)

    # Max 2 hard days/week: downgrade Tue quality if Sunday's long run is already hard, or there's a Sat TT.
    hard_sun = sun_type == "race" or w in HARD_LR
    is_tt_week = w in (1, 9)
    if tue_type == "quality" and (hard_sun or is_tt_week):
        tue_txt, tue_type = "Easy 30 min, deliberately easy", "easy"

    days = {}
    days["Mon"] = ("Rest — always", "rest", 0)
    tue_km = 0 if tue_type == "rest" else round(v * 0.14, 1)
    thu_km = 0 if thu_type == "rest" else round(v * 0.14, 1)
    wed_km = 0 if wed_type == "rest" else round(v * 0.10, 1)
    known = lr + tue_km + thu_km + wed_km + ((sat_fixed or 0) if w in (1, 9) else 0)
    if w == 19:
        known = lr
    sat_pool = max(round(v - known, 1), 0)

    days["Tue"] = (tue_txt + ("  +S&C A" if w >= 3 and tue_type != "rest" else ""), tue_type, tue_km)
    days["Wed"] = (wed_txt, wed_type, wed_km)
    days["Thu"] = (thu_txt + ("  +S&C B" if w >= 3 and thu_type != "rest" else ""), thu_type, thu_km)
    days["Fri"] = ("Rest — always", "rest", 0)
    if w == 19:
        days["Sat"] = (sat_txt, sat_type, 3)
    elif sat_txt is None:
        days["Sat"] = (f"Easy {sat_pool} km + strides", "easy", sat_pool)
    else:
        days["Sat"] = (sat_txt, sat_type, sat_fixed if sat_fixed else sat_pool)
    days["Sun"] = (sun_txt, sun_type, round(lr, 1))
    return days


def focus(w):
    return {1: "Baseline time trial — everything else is built off this", 4: "Cut-back",
            8: "Cut-back", 9: "Optional 10K check-in", 12: "Cut-back",
            15: "Peak long run — biggest test before taper", 16: "Cut-back",
            19: "RACE WEEK"}.get(w, "")


DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def content():
    return {
        "paces": {"headers": ["Zone", "Effort", "Use"], "rows": [
            ["Easy / aerobic", "Fully conversational — could hold a chat", "Bulk of every week"],
            ["Long-run easy", "Conversational, slightly more effort by the end", "Long-run base pace"],
            ["Steady / controlled", "Comfortably hard — a sentence at a time, not a chat", "Long-run finishes, tempo work"],
            ["Time-trial / race effort", "All-out, sustainable for the distance", "Week 1 & 9 checkpoints, race day"]],
            "note": "No fixed pace numbers here on purpose — week 1's time trial sets your real baseline, and "
                    "from there effort (not a number picked before you'd run a step) drives every session. "
                    "Once you have a few checkpoints in, ask for actual pace targets and they can be added."},
        "checkpoints": {
            "intro": "No fixed goal time — the point of these is simply to show you the trend, so race day is "
                     "informed by real data, not a guess made in week 1.",
            "headers": ["Wk / date", "Test", "What it tells you"], "rows": [
                ["Wk 1 · this Saturday", "5K time trial / parkrun", "Sets your real baseline — everything else calibrates off this"],
                ["Wk 9 · ~27 Sep", "10K time trial (optional)", "Shows how much the aerobic base has moved the needle"],
                ["Wk 15 · ~1 Nov", "Peak long run (19 km, last 6 km steady)", "The honest read on race-day pacing strategy"],
                ["Race · 6 Dec", "Sevilla Half Marathon", "Run it off what training actually showed, not a number from July"]],
            "notes": [
                "This is a genuine from-scratch build — 5 running days a week (Tue/Wed/Thu/Sat/Sun), Monday and "
                "Friday always off.",
                "No pressure toward a specific time — \"best she can\" is a completely legitimate goal, and it "
                "means the plan can flex around how the weeks actually go rather than forcing a number.",
                "Long run peaks at 19 km, not the full 21.1 — race-day adrenaline and taper freshness reliably "
                "cover the last bit.",
                "Once the Wk-1 time trial lands, actual pace numbers can replace the effort-based zones above "
                "if that's useful — just ask."]},
        "strength": C.strength("1–8", "9–16", football=False),
        "fuel": C.fuel(football=False, volume_note=""),
        "research": C.RESEARCH_NOTES,
        "tips": [
            ["The time trial matters more than it feels like", "Week 1's 5K sets the baseline for everything else in this plan — go in fresh and actually push it, don't just jog it."],
            ["No goal time is a real goal", "\"Best I can, off real training\" is a completely legitimate target — it just means racing off what the checkpoints actually show, not a number guessed before a single run."],
            ["Consistency over the first month is everything", "The first 4 weeks are about building the habit as much as the fitness — showing up matters more than any single session's quality."],
        ] + C.TIPS_COMMON,
    }


def build():
    weeks = []
    for w in range(1, 20):
        monday = START + timedelta(days=(w - 1) * 7)
        dm = build_week(w)
        days = []
        for i, dow in enumerate(DOW):
            txt, typ, km = dm[dow]
            days.append({"date": (monday + timedelta(days=i)).isoformat(), "dow": dow,
                         "type": typ, "session": txt, "target_km": km})
        weeks.append({"week": w, "start": monday.isoformat(), "phase": phase(w),
                      "target_km": VOL[w - 1], "focus": focus(w), "days": days})
    return {"meta": {"id": ID, "name": NAME, "goal": GOAL, "mp_per_km": "TBD", "mp_per_mile": "TBD",
                    "start": START.isoformat(), "race": RACE.isoformat(),
                    "peak_km": max(VOL), "total_weeks": 19,
                    "goal_note": "No fixed goal pace — Week 1's time trial sets the real baseline, and the "
                                 "checkpoints (Wk 9, Wk 15) build the picture from there."},
            "weeks": weeks, "content": content()}
