"""Shared reference content (Strength, Fuel & Life, common Tips) for the dashboards.
Runner-specific Paces/Checkpoints/Goals live in each runner module."""

SC_FOUNDATION = [
    ["Goblet squat", "3 × 10", "Full depth, controlled — base leg strength"],
    ["Rear-foot-elevated split squat", "3 × 8 / leg", "Unilateral — knee tracks over toe"],
    ["Romanian deadlift (DB/BB)", "3 × 8", "Hip hinge — hamstrings & glutes"],
    ["Single-leg calf raise (straight knee)", "3 × 12 / leg", "Slow lower — Achilles/gastroc resilience"],
    ["Bent-knee calf raise (soleus)", "3 × 15 / leg", "Soleus — the runner's forgotten muscle"],
    ["Glute bridge / hip thrust", "3 × 12", "Squeeze glutes — power & posture"],
    ["Copenhagen plank", "3 × 20s / side", "Adductor/groin strength (injury shield)"],
    ["Side plank", "3 × 30s / side", "Lateral hip stability"],
    ["Dead bug", "3 × 8 / side", "Core without arching the lower back"],
]
SC_POWER = [
    ["Back or front squat", "4 × 5", "Heavier but crisp — max strength"],
    ["Trap-bar / conventional deadlift", "3 × 5", "Strong hinge, full body"],
    ["Bulgarian split squat (loaded)", "3 × 6 / leg", "Loaded unilateral strength"],
    ["Nordic / eccentric hamstring curl", "3 × 5", "#1 hamstring-injury preventer"],
    ["Single-leg calf raise (loaded)", "3 × 10 / leg", "Tendon stiffness = economy"],
    ["Pogo hops / ankle bounces", "3 × 20", "Springy ankles — free speed"],
    ["Box jumps or bounding", "3 × 5", "Power — land soft; skip if legs cooked"],
    ["Hip thrust (loaded)", "3 × 8", "Glute power for late-race drive"],
]
SC_TAPER = [
    ["Bodyweight circuit (squat, calf raise, bridge, plank)", "1–2 × light", "Keep the pattern, add zero fatigue"],
    ["No plyometrics / heavy loads", "—", "Stop ALL strength 5–7 days before race day"],
]
SC_PREHAB = [
    ["Calf raises (straight + bent knee)", "2 × 15", "Achilles/soleus armour as load ramps"],
    ["Tibialis raises (toes up)", "2 × 20", "Prevent shin splints"],
    ["Knee-to-wall ankle mobility", "1 × 10 / side", "Dorsiflexion for stride"],
    ["Couch stretch / hip flexor", "30s / side", "Undo desk-sitting"],
    ["Foam roll calves, quads, glutes", "2–3 min", "As needed for tight spots"],
]
SC_HEADERS = ["Exercise", "Sets × Reps", "Cue / why"]

WARMUP_ROUTINE = [
    ["Easy cardio (bike/row/jog)", "2 min", "Raise pulse and core temperature before anything else — "
     "cold muscles/tendons are exactly when niggles start."],
    ["Leg swings — front-to-back", "10 / leg", "Dynamic hip mobility, sagittal plane."],
    ["Leg swings — side-to-side", "10 / leg", "Dynamic hip/adductor mobility, frontal plane."],
    ["Walking lunge with a twist", "8 / leg", "Hip flexor + quad prep, plus a bit of rotational core."],
    ["Glute bridge (fast, bodyweight)", "15", "Wake the glutes up before they get asked to work — "
     "quiet glutes are how load ends up somewhere it shouldn't."],
    ["Banded lateral walks (monster walks)", "10 steps / direction", "Glute medius + hip stability — "
     "directly protects against the lateral ankle/peroneal issues that come from poor hip control."],
    ["Ankle eversion band work", "15 / side", "Peroneal activation — the specific prehab for the outside-"
     "ankle stiffness/soreness, do this one even on days it feels fine."],
    ["Single-leg balance", "20s / side", "Proprioception — the single best-evidenced intervention for "
     "lateral ankle stability generally, not just when something's already sore."],
    ["Dynamic calf raises", "15", "Ankle/Achilles complex prep — last thing before you load anything heavier."],
]
WARMUP_HEADERS = ["Exercise", "Duration / Reps", "Why"]


def note_wu(txt, typ):
    """A quality session's km target is the WHOLE session (warm-up + reps/tempo + jog
    recoveries + cooldown), not just the structured work described in the text — e.g. a
    13 km session built around 5x1km reps has ~7 km of warm-up/cooldown/jog around that
    5 km of hard running. Flag it in the text so the number doesn't read as a mismatch.
    Skip sessions that already state their own total ("Medium-long 16 km w/ middle 8 km
    @ MP") — adding the note there would double up rather than clarify."""
    if typ != "quality" or "w/u" in txt:
        return txt
    if txt.startswith("Medium-long") or " km w/" in txt:
        return txt
    return txt + " + w/u & c/d"


def strength(found_weeks, power_weeks, football=False, a_day="Tue", b_day="Fri"):
    extra = " or a match" if football else ""
    return {
        "intro": ("2×/week, 20–35 min. Injury-proof tendons/hips + improve running economy. "
                  f"Never heavy legs before a long run{extra}. Form first, load second."),
        "sessions": {"headers": ["Session", "Day", "What it is"], "rows": [
            ["Hard-day session", a_day, f"Straight after your {a_day} quality session"],
            ["Easy-day session", b_day, f"After your {b_day} recovery run — same exercises as the "
                                         "hard-day session, whichever phase block below you're currently in"],
        ]},
        "blocks": [
            {"title": f"Foundation · Weeks {found_weeks}", "headers": SC_HEADERS,
             "note": "Build tissue tolerance, bodyweight → light load. 2×/week.", "rows": SC_FOUNDATION},
            {"title": f"Strength & Power · Weeks {power_weeks}", "headers": SC_HEADERS,
             "note": "Heavier + a little spring for economy & late-race power. 2×/week.", "rows": SC_POWER},
            {"title": "Taper · Weeks 31–33", "headers": SC_HEADERS,
             "note": "Maintain only — no fatigue. 1×/week max.", "rows": SC_TAPER},
            {"title": "Daily prehab · 5 min, most days", "headers": SC_HEADERS,
             "note": "Little-and-often — keeps you on the road while mileage climbs.", "rows": SC_PREHAB},
        ],
    }


FUEL_DIET = [
    ["Carbs fuel the work", "Your main running fuel — don't fear it. More around long/quality days."],
    ["Protein for repair", "~1.6–2.0 g/kg/day across meals — repairs muscle & tendon as you build."],
    ["Don't under-fuel", "As mileage rises, under-eating causes injury, illness and burnout. Eat enough."],
    ["Wholefoods base", "Veg, fruit, whole grains, quality protein, healthy fats. Check iron if chronically flat."],
]
FUEL_PRE = [
    ["Easy short runs (<60 min)", "Fine fasted or light — coffee + banana."],
    ["Long & quality runs", "Fuel first: a carb meal 2–3 h before (porridge + banana, toast + eggs), low fat/fibre."],
    ["30–60 min before", "Quick top-up if needed: banana, toast + jam, or a gel."],
    ["Coffee ~45–60 min before", "Caffeine is a legit, legal boost before hard sessions and races."],
]
FUEL_POST = [
    ["Recovery window", "After long/quality runs: carbs + 20–30 g protein within ~60 min."],
    ["Rehydrate", "Replace ~1.25–1.5× fluid lost; add salt if you're a salty/heavy sweater."],
]
# Carbs DURING the run. The ceiling here is your gut, not your legs, and unlike most of
# this page it's a skill that has to be trained over months — which means it belongs in
# the plan from the first long run, not bolted on in race week.
FUEL_CARBS = [
    ["Under 75 min", "Nothing needed. Water only."],
    ["75–120 min", "30–40 g carbs/hr — one feed around 45 min, one around 90."],
    ["2:00–2:30", "50–60 g/hr, something every 25–30 min."],
    ["2:30 and beyond", "70–90 g/hr, every 20 min. Needs glucose AND fructose together — glucose alone saturates its transporter near 60 g/hr, however much you swallow."],
    ["Start at 40–45 min", "Not when you feel empty. Absorption is rate-limited, so once you're behind you cannot catch up — you can only slow down."],
    ["Train the gut", "Tolerance takes months, and it's pace-specific: carbs you handle fine at easy pace can come straight back up at MP. Build from 30–40 g/hr now toward 70–90 by the peak block."],
    ["Rehearse at race pace", "At least two long runs with MP segments AND full race fuelling. A gel at easy pace proves nothing about a gel at marathon pace."],
    ["Slower finish, more total fuel", "Per-hour rates don't change, but a 4:00 marathon is four hours of fuelling against three. Total need scales with time on feet, not distance."],
]
# Fluid and sodium are a separate problem from carbs and in heat they bite first.
FUEL_FLUID = [
    ["Measure yours — once", "Weigh yourself naked before and after a long run and note what you drank. Sweat loss (L) = kg lost + litres drunk. Do it on a hot run and a cool one; those two numbers beat any general guidance here."],
    ["Cool, 15–18°C", "300–400 ml/hr."],
    ["Warm, 22–25°C", "500–700 ml/hr."],
    ["Hot, ~30°C", "700–1,000 ml/hr — and accept you'll still finish down on the day."],
    ["The 2% rule", "Lose more than 2% of body weight in fluid and both performance and heat regulation fall away sharply."],
    ["Don't overdrink either", "Large volumes of plain water in heat dilute blood sodium. That is genuinely dangerous, not merely suboptimal."],
    ["Sodium 500–1,000 mg/hr", "In heat. White crust on your cap or sunglasses and stinging eyes mean you're a salty sweater — work at the top of that range."],
    ["Heat distorts the data", "A run finishing above ~25°C measures heat tolerance, not fitness: HR sits 10–15 bpm higher for the same effort. Judge sessions, and time trials, on the cool ones."],
]
# Almost none of this needs branded product. Sucrose is glucose+fructose bonded 1:1,
# which is the ratio the expensive mixes are sold on.
FUEL_CHEAP = [
    ["Table sugar is the answer", "Sucrose IS glucose + fructose, bonded 1:1 — essentially the ratio brands charge a premium for, and it performs the same in head-to-head studies."],
    ["The recipe, per 750 ml", "45 g sugar (3 heaped tbsp) + ¼ tsp table salt (~590 mg sodium) + squash or lemon to make it drinkable. That's 45 g carb at ~6%."],
    ["Keep it at 6% or below", "Stronger than that in heat and it sits in your stomach instead of emptying into the gut."],
    ["What it costs", "About €0.03 per 25 g of carbohydrate, against €1.80–4.00 for a gel. A €1 bag of sugar covers most of a training block."],
    ["Cheap solid options", "Dates (~75 g carb/100 g — best value real food), jelly babies or Haribo, fig rolls, raisins, white bread and jam."],
    ["Flat Coca-Cola", "Late in long runs. Sugar plus caffeine, and it goes down when nothing else will."],
    ["Caffeine tablets", "Pennies against caffeinated gels. ~3 mg/kg an hour before a hard session or race."],
    ["Electrolyte on the cheap", "Oral rehydration sachets from any pharmacy (in Spain, ask for 'suero oral') — same ingredients as tablets at a fraction of the price."],
    ["Still buy one or two gels", "Try them once, so you know whether you can stomach what's on the course table when that's all there is."],
    ["Carrying it for nothing", "Loop the route past home or the car and stash a bottle — a 7 km loop run three times needs no kit at all. A 500 ml soft flask (~€10) is the only thing worth buying before you're running 30 km in heat."],
]
FUEL_ALC = [
    ["What it costs you", "Wrecks deep sleep, dehydrates, blunts recovery, raises next-day injury risk."],
    ["Timing rule", "If you drink, do it after a hard session / before a rest day — never before a long run, quality day or race."],
    ["Race week", "Minimise in the last 2 weeks; zero in race week."],
]
FUEL_DECIDE = [
    ["Hungover", "Skip quality & long runs (dehydration + poor coordination = injury). Full rest or an easy jog only if mild and rehydrated first. Reschedule the key session; don't cram it back."],
    ["Injured — niggle", "Pain that changes your stride or worsens as you run → STOP. 2–3 easy/off days now beats weeks off later. Sharp/one-sided/joint pain → rest & assess. Cross-train pain-free to keep fitness."],
    ["Injured — not improving", "Not better in a few days, or worse? See a physio early — don't 'test it' with a hard run."],
    ["Ill — neck rule", "Above the neck (runny nose, mild throat) → easy run usually OK. Below the neck (chest, fever, aches) → REST. NEVER run with a fever."],
    ["Wrecked / under-recovered", "Heavy legs, rising resting HR, poor sleep = under-recovery. Take the easy day easy or swap to rest. Missing one session to absorb training is smart."],
]


def warmup(niggle_note=None):
    """A ~8 min dynamic warm-up/activation routine to do before EVERY gym session — not a
    substitute for the strength blocks above, the thing that comes before them."""
    intro = ("Do this before every gym session (3-4x/week), before you touch a bar or a run. "
             "~8 minutes. Dynamic movement, not static stretching — static holds before training "
             "don't reduce injury risk the way people assume, and can blunt power output short-term. "
             "Consistency matters more than any single exercise here — this only works if it happens "
             "every time, not just when something already hurts.")
    if niggle_note:
        intro += f" {niggle_note}"
    return {"intro": intro, "headers": WARMUP_HEADERS, "rows": WARMUP_ROUTINE}


def fuel(football=False, volume_note=""):
    decide = list(FUEL_DECIDE)
    if football:
        decide.append(["Big football week", "If a match or tournament ate your legs, downgrade the next run to easy/recovery and protect the long run. Two hard efforts a week total — matches included."])
    intro = ("You can't out-train poor fuelling, sleep or recovery" + (f" — {volume_note}" if volume_note else "") +
             ". Fuel the work, protect recovery, be smart about alcohol, and know when NOT to run. "
             "Fuelling a long run is a trained skill, not a race-day decision: the gut adapts over "
             "months, so practise it from the first long run rather than discovering your limits at 30 km.")
    return {
        "intro": intro,
        "sections": [
            {"title": "Daily diet · fuel the work", "headers": ["Topic", "Detail"], "rows": FUEL_DIET},
            {"title": "Before running · what & when", "headers": ["Topic", "Detail"], "rows": FUEL_PRE},
            {"title": "During the run · carbs", "headers": ["Duration / rule", "Detail"], "rows": FUEL_CARBS},
            {"title": "During the run · fluid & sodium", "headers": ["Conditions / rule", "Detail"], "rows": FUEL_FLUID},
            {"title": "Doing it cheaply · sugar beats gels", "headers": ["Topic", "Detail"], "rows": FUEL_CHEAP},
            {"title": "After · recover & rehydrate", "headers": ["Topic", "Detail"], "rows": FUEL_POST},
            {"title": "Alcohol · the honest version", "headers": ["Topic", "Detail"], "rows": FUEL_ALC},
            {"title": "Should I run today? · quick guide", "headers": ["Situation", "What to do"], "rows": decide},
        ],
    }


RESEARCH_NOTES = {
    "intro": "This plan isn't arbitrary — the phase structure, cut-back placement, hard/easy alternation and "
             "rest-day rules below are each grounded in specific training-science sources, reviewed 2026-07.",
    "sections": [
        {"title": "Phase structure (5 mesocycles)",
         "detail": "Base/Aerobic → Threshold intro → Lactate-Threshold + MP intro → Marathon-Specific (peak) → "
                    "Taper. This matches the consensus shape across Jack Daniels (Running Formula phases I–IV), "
                    "Pete Pfitzinger (Advanced Marathoning: Base / LT / Race-Prep / Taper), and Renato Canova's "
                    "funnel model (General → Fundamental → Special → Specific → short taper) — all converge on "
                    "4–5 phases for a build this long, with taper length staying fixed at 2–3 weeks regardless "
                    "of total plan length."},
        {"title": "Cut-back (deload) weeks",
         "detail": "Placed every ~3–6 weeks, cutting volume ~15–25%. Sourced from Pfitzinger's step-back weeks "
                    "and the broader coaching consensus (Laura Norris, RunnersConnect) of 15–33% volume drops "
                    "every 3–4 weeks to let fitness consolidate before the next load increase."},
        {"title": "Hard/easy long-run alternation (added 2026-07-16)",
         "detail": "Marathon-pace long runs now strictly alternate with easy long runs — no two hard long-run "
                    "weekends back-to-back, and the weekends either side of each tune-up half are forced easy. "
                    "Basis: single-run distance/intensity spikes are a stronger injury predictor than weekly-"
                    "volume jumps (JOSPT running-injury literature), and \"shock microcycles\" (stacking hard "
                    "efforts) are explicitly not recommended for sub-elite runners — steady progressive/"
                    "undulating loading with regular relief outperforms them for this population."},
        {"title": "Max 2 hard days per week",
         "detail": "Quality sessions are capped at two per week (e.g. Tue quality + EITHER Thu quality OR a hard "
                    "Sunday MP long run, never all three) — consistent with polarized/pyramidal training research "
                    "(Stephen Seiler) showing the bulk of volume should stay easy even as the marathon-specific "
                    "phase shifts intensity distribution from ~80/20 toward ~70/30 threshold-and-MP-heavy work."},
        {"title": "Rest days fixed to Monday + Saturday",
         "detail": "Runner preference, applied without compromising the two hard-day cap or long-run "
                    "alternation above."},
        {"title": "Marathon-pace (MP) progression timing",
         "detail": "MP segments enter the long run roughly 6–8 weeks before the peak-volume block, starting "
                    "short and building toward the largest MP-block long runs at peak — the standard Pfitzinger/"
                    "Hansons/Luke Humphrey pattern for when MP-specific work pays off without excess injury risk."},
        {"title": "Taper",
         "detail": "3-week taper, volume cut cumulatively (~roughly 75% → 50% → 30–35% of peak by race week), "
                    "intensity maintained and session frequency cut ≤20% — the most robust finding in the taper "
                    "literature (Mujika & Padilla's taper meta-analyses)."},
        {"title": "Altitude training — considered, not included",
         "detail": "Discussed 2026-07-16: a single week at altitude gives none of the hematological benefit "
                    "(EPO/red-cell-mass adaptations need a minimum ~3–4 weeks per Levine & Stray-Gundersen's "
                    "\"live high, train low\" research) and mostly adds hypoxic stress, poor sleep and slower "
                    "paces at the wrong moment. Verdict: skip a 1-week trip; a proper 3+ week camp placed in "
                    "the aerobic-base phase would be worth a separate conversation if it becomes an option."},
    ],
}

TIPS_COMMON = [
    ["Easy means EASY", "Most running should be conversational — even slower than feels 'proper'. That's where the engine is built."],
    ["The niggle rule", "Pain that changes your gait or worsens = stop. 2–3 easy/off days early beats 3 weeks off later."],
    ["Guard the long run", "The single most important marathon session — the last thing to sacrifice when the week gets messy."],
    ["Sleep is the #1 recovery tool", "7–9 h/night. Higher volume needs more recovery, not less."],
    ["Fuel the long ones", "Past 75 min take carbs on board and rehearse your race-day breakfast. Rates scale with duration — see Fuel & life for the full table."],
    ["Rotate 2 pairs of shoes", "Cuts injury risk, extends shoe life (~500–800 km). Buy race shoes by the tune-up and run 3–4 sessions in them."],
    ["Warm up the hard day", "10–15 min easy + a few strides before any tempo/threshold/VO2 work."],
    ["Respect cut-back weeks", "The down weeks are when fitness consolidates — don't 'top them up'."],
    ["Calibrate at the half", "The tune-up half sets your real race pace. Race the pace you EARNED, not the dream."],
    ["Start the race easy", "First few km should feel too easy. Hold back — the marathon starts at 30 km. Even pacing wins."],
    ["Race-day fuel clock", "Feed every 20–30 min from ~45 min in, with water — target 70–90 g carbs/hr over a marathon. Don't wait until you're empty."],
    ["Tokyo in early March", "~8–12°C, flat, fast — a great course. Dress for ~+10°C warmer than standing; throwaway layer at the start."],
    ["Nothing new two weeks out", "No new shoes, foods or bonus sessions. Lock the routine and trust the work."],
    ["Log everything", "Fill it in after each run — it keeps you honest and shows patterns before they become problems."],
]
