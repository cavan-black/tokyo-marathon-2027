"""Stephen's sub-2:00 half marathon plan as structured data. build() -> plan dict.
62, currently 98 kg, has a 4:01 marathon PR but starting essentially from scratch —
run-walk foundation building to continuous running, dual goal of sub-2:00 AND weight
loss. 19-week build to the Sevilla Half (6 Dec 2026), same race Cav is tuning up at
and Jamie is using as a training run."""
from datetime import date, timedelta
import content as C

ID, NAME, GOAL = "stephen", "Stephen", "Sub-2:00 half"
START = date(2026, 7, 27)
RACE  = date(2026, 12, 6)

# Total session distance (run-walk counts as covered distance, not just "running" km).
VOL = [10, 12, 14, 15,
       17, 19, 22, 24,
       27, 30, 33, 36,
       39, 42, 44, 40,
       32, 24, 16]
LR  = [3, 4, 5, 5,
       6, 7, 8, 9,
       10, 11, 13, 14,
       16, 17, 18, 15,
       12, 8, 21.0975]

# Long-run weekends with a bit more sustained effort — always alternate with an easy one.
HARD_LR = {11, 13, 15}
CUTBACK = {4, 8, 12, 16}


def phase(w):
    if w <= 4:  return "Run-walk foundation"
    if w <= 8:  return "Continuous running"
    if w <= 12: return "Endurance build"
    if w <= 16: return "Half-specific peak"
    return "Taper & race"


def run_walk(w):
    """Run:walk interval prescription — progresses toward continuous running by week 13."""
    lib = {
        1: "8 x (run 1min / walk 2min)", 2: "8 x (run 1min / walk 2min)",
        3: "8 x (run 2min / walk 2min)", 4: "6 x (run 2min / walk 2min) — cut-back",
        5: "8 x (run 3min / walk 1min)", 6: "8 x (run 3min / walk 1min)",
        7: "6 x (run 5min / walk 1min)", 8: "5 x (run 5min / walk 1min) — cut-back",
        9: "4 x (run 8min / walk 1min)", 10: "4 x (run 8min / walk 1min)",
        11: "3 x (run 10min / walk 1min)", 12: "3 x (run 10min / walk 1min) — cut-back",
    }
    return lib.get(w)


def tue(w):
    rw = run_walk(w)
    if rw:
        return f"Run-walk: {rw}", "easy"
    if w <= 16:
        lib = ["Easy continuous 25-30 min, walk breaks as needed", "Steady 30 min, negative split second half",
               "Easy continuous 30-35 min", "Steady 30 min + 4 x 1min pickups (not flat out)"]
        return lib[(w - 13) % len(lib)], ("quality" if "pickups" in lib[(w - 13) % len(lib)] else "easy")
    return {17: "Easy 25 min, relaxed", 18: "Easy 20 min + a few strides",
            19: "Rest or 10 min shakeout"}[w], "easy"


def thu(w):
    rw = run_walk(w)
    if rw:
        return f"Run-walk: {rw}", "easy"
    if w <= 16:
        lib = ["Easy continuous 25 min", "Easy continuous 30 min", "Steady 30-35 min, conversational",
               "Easy continuous 30 min"]
        return lib[(w - 13) % len(lib)], "easy"
    txt = {17: "Easy 20 min", 18: "Rest", 19: "Rest"}[w]
    return txt, ("rest" if txt == "Rest" else "easy")


def sat(w):
    rw = run_walk(w)
    if rw:
        return f"Run-walk: {rw} (shorter than Sunday)", "easy"
    if w <= 16:
        return "Easy continuous 25-30 min, truly conversational", "easy"
    return {17: "Easy 20 min + strides", 18: "Easy 15 min",
            19: "Shakeout 10-15 min + a few strides"}[w], "easy"


def sun(w):
    d = LR[w - 1]
    txt = {
        11: f"{d:g} km — first continuous long run with NO walk breaks planned (walk if you truly need to)",
        12: f"{d:g} km easy — cut-back, protect the knees before the peak block",
        13: f"{d:g} km, last 3 km at a steady, controlled effort",
        15: f"{d:g} km, last 5 km at a steady, controlled effort — biggest test before taper",
        16: f"{d:g} km easy — cut-back",
        19: "RACE DAY — Sevilla Half Marathon · sub-2:00 target · 5:41/km · 9:09/mi",
    }
    t = txt.get(w, f"{d:g} km — {'run-walk, whatever ratio feels controlled' if w <= 10 else 'easy continuous'}")
    return t, ("race" if w == 19 else "long")


def qkm(w):
    if w <= 12: return LR[w - 1] * 0.55  # run-walk sessions are naturally shorter than the long run
    return {13: 6, 14: 6, 15: 6, 16: 5, 17: 4, 18: 3, 19: 2}.get(w, 6)


def build_week(w):
    v = VOL[w - 1]
    lr = LR[w - 1]
    tue_txt, tue_type = tue(w)
    thu_txt, thu_type = thu(w)
    sun_txt, sun_type = sun(w)
    sat_txt, sat_type = sat(w)
    q = round(qkm(w), 1)
    tue_km = q
    thu_km = 0 if thu_type == "rest" else q
    days = {}
    days["Mon"] = ("Rest — always", "rest", 0)
    days["Tue"] = (tue_txt + ("  +S&C (hard-day session, joint-friendly)" if w >= 3 else ""), tue_type, tue_km)
    days["Wed"] = ("Rest, or an easy 20-30 min walk/swim/bike (low impact, protects the weight-loss deficit"
                   " without adding running-specific fatigue)", "rest", 0)
    days["Thu"] = (thu_txt + ("  +S&C (easy-day session, joint-friendly)" if w >= 3 and w != 18 and w != 19 else ""),
                   thu_type, thu_km)
    days["Fri"] = ("Rest — always", "rest", 0)
    if w == 19:
        sat_km = 2  # race-week shakeout, nominal distance
    else:
        sat_km = max(round(v - lr - tue_km - thu_km, 1), 1)
    days["Sat"] = (sat_txt, sat_type, sat_km)
    days["Sun"] = (sun_txt, sun_type, round(lr, 1))
    return days


def focus(w):
    return {4: "Cut-back — let the run-walk foundation settle", 8: "Cut-back",
            11: "First continuous long run — no walk breaks planned", 12: "Cut-back",
            15: "Peak long run — biggest test before taper", 16: "Cut-back",
            19: "RACE WEEK"}.get(w, "")


DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def content():
    return {
        "banner": ("Before you start: at 62 with a higher starting bodyweight and coming back from a long "
                   "layoff, a quick GP/health check before ramping up is a sensible box to tick — not because "
                   "anything's wrong, just standard due diligence for restarting vigorous exercise at this "
                   "profile. Nothing here should hurt; if something does, that's the signal to ease off, not "
                   "push through."),
        "paces": {"headers": ["Zone", "per km", "per mile", "Use"], "rows": [
            ["Walk (in run-walk)", "—", "—", "Full recovery between run intervals — genuinely easy walking"],
            ["Easy / aerobic", "7:00–8:00", "11:16–12:52", "Bulk of running once continuous (from ~wk 9)"],
            ["Long-run easy", "6:50–7:40", "11:01–12:19", "Long-run base pace"],
            ["Half-marathon (target)", "5:41", "9:09", "Sub-2:00 pace — only once wk-13/15 checkpoints confirm it"],
            ["Steady / controlled", "6:15–6:40", "10:03–10:44", "The controlled-effort finishes on big long runs"]],
            "note": "Every pace above assumes the run-walk foundation (weeks 1-8) is genuinely easy — this "
                    "phase is about building tissue tolerance and consistency, not fitness tests. Sub-2:00 "
                    "pace only enters the picture once you're running continuously and the checkpoints say "
                    "it's realistic."},
        "checkpoints": {
            "intro": "Sub-2:00 is the target, but it's provisional — the honest read comes from weeks 11 and "
                     "15. If the numbers say a different goal is more realistic, that's useful information, "
                     "not a failure.",
            "headers": ["Wk / date", "Test", "On track for sub-2:00", "If short — be honest about it"], "rows": [
                ["Wk 11 · ~5 Oct", "First continuous long run (13 km)", "Comfortable, controlled finish",
                 "Still needing walk breaks → that's fine, it just means sub-2:00 may need more time"],
                ["Wk 15 · ~2 Nov", "Peak long run (18 km, last 5 km steady)", "Steady km's at ~5:50-6:10/km",
                 "Struggling past 12-13 km → aim for a strong finish over a fast one on race day"],
                ["Race · 6 Dec", "Sevilla Half Marathon", "Sub-2:00 = 5:41/km", "Finishing strong beats blowing up at 15 km"]],
            "notes": [
                "This plan is genuinely from scratch — the run-walk phase (weeks 1-8) is not optional filler, "
                "it's what lets you get to continuous running without a stress-fracture or knee flare-up.",
                "4 running days/week (Tue/Thu/Sat/Sun), not 6 — more recovery time between sessions at 62 is a "
                "feature, not a compromise.",
                "Weight loss and running fitness both improve fastest with consistency, not intensity — showing "
                "up 4x/week beats occasional heroics.",
                "Long run peaks at 18 km, not the full 21.1 — race-day adrenaline, taper freshness and crowd "
                "energy reliably cover the gap; you don't need to have run the full distance in training."]},
        "strength": C.strength("1–8", "9–16", football=False, b_day="Thu"),
        "fuel": {
            "intro": "Two goals at once — losing weight AND building running fitness — are compatible, but only "
                     "with a moderate deficit. Aggressive dieting on top of a new training load is how people "
                     "get injured, exhausted, or both; slow and sustainable wins here.",
            "sections": [
                {"title": "The deficit — moderate, not aggressive", "headers": ["Topic", "Detail"], "rows": [
                    ["Target rate", "~0.3-0.5 kg/week. Faster than that risks muscle loss and under-fuelled runs."],
                    ["Protein first", "~1.6-2.0 g/kg/day — protects muscle mass while in a deficit, especially important at 62."],
                    ["Don't diet on run days", "Fuel properly around Tue/Thu/Sat/Sun sessions — the deficit should come from rest-day/general eating, not from skimping around training."],
                    ["Weigh weekly, not daily", "Day-to-day water/food weight swings are noise — trust the 3-4 week trend."],
                ]},
                {"title": "Before running", "headers": ["Topic", "Detail"], "rows": [
                    ["Run-walk sessions (short)", "Fine fasted or with just a coffee if that's your routine."],
                    ["Long runs (Sunday)", "A small carb-containing snack 60-90 min before once sessions pass ~45 min — banana, toast."],
                ]},
                {"title": "During & after", "headers": ["Topic", "Detail"], "rows": [
                    ["Long runs over 60 min", "Water + a bit of carb (gel, sports drink, or dates) once past week 11's continuous long runs."],
                    ["Recovery", "Protein within an hour or two of the longer sessions — supports the muscle-preservation goal above."],
                ]},
                {"title": "Should I run today? · quick guide", "headers": ["Situation", "What to do"], "rows": [
                    ["Joint niggle (knee/hip/ankle)", "STOP for that session. At 98 kg + 62, a niggle you run through becomes an injury that costs weeks — a niggle you rest often resolves in days."],
                    ["Just tired / unmotivated", "Go anyway, but make it the easiest version of the session — this plan has a lot of built-in slack for exactly this."],
                    ["Genuinely exhausted / poor sleep", "Skip it. One missed run-walk session changes nothing; a week of poor recovery compounding does."],
                    ["Ill", "Above the neck (cold) → fine to try an easy session. Fever or chest symptoms → full rest, no exceptions."],
                ]},
            ],
        },
        "research": C.RESEARCH_NOTES,
        "tips": [
            ["Run-walk isn't a lesser method", "It's the standard, well-evidenced way to build running fitness from a deconditioned start — it lets your cardiovascular system adapt faster than your joints/tendons can tolerate continuous impact, so you progress without breaking down."],
            ["Consistency beats intensity here", "4 sessions/week for 19 weeks, done, beats an ambitious plan abandoned in week 6 after an injury."],
            ["The marathon experience helps more than you'd think", "Pacing discipline and fuelling habits from your 4:01 don't disappear — lean on that even while the fitness rebuilds."],
            ["Sub-2:00 is a real target, not a stretch fantasy", "9:29/km average is very achievable off a genuine 19-week build for someone with your endurance background — just let the checkpoints (not week 1 optimism) confirm it."],
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
    return {"meta": {"id": ID, "name": NAME, "goal": GOAL, "mp_per_km": "5:41", "mp_per_mile": "9:09",
                    "start": START.isoformat(), "race": RACE.isoformat(),
                    "peak_km": max(VOL), "total_weeks": 19,
                    "goal_note": "Sub-2:00 half (5:41/km) — provisional until the Wk-11 and Wk-15 checkpoints "
                                 "confirm it. From-scratch build: run-walk through week 8, continuous from week 9."},
            "weeks": weeks, "content": content()}
