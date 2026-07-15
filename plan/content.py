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


def strength(found_weeks, power_weeks, football=False):
    extra = " or a match" if football else ""
    return {
        "intro": ("2×/week, 20–35 min. Injury-proof tendons/hips + improve running economy. "
                  f"TIMING: after runs, on your hard day (Tue = Session A) + one easy day (Fri = Session B). "
                  f"Never heavy legs before a long run{extra}. Form first, load second."),
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
    ["During (>90 min)", "40–60 g carbs/hr (gels/drink) + fluids. Start early, don't wait to feel empty."],
    ["Recovery window", "After long/quality runs: carbs + 20–30 g protein within ~60 min."],
    ["Rehydrate", "Replace ~1.25–1.5× fluid lost; add salt if you're a salty/heavy sweater."],
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


def fuel(football=False, volume_note=""):
    decide = list(FUEL_DECIDE)
    if football:
        decide.append(["Big football week", "If a match or tournament ate your legs, downgrade the next run to easy/recovery and protect the long run. Two hard efforts a week total — matches included."])
    intro = ("You can't out-train poor fuelling, sleep or recovery" + (f" — {volume_note}" if volume_note else "") +
             ". Fuel the work, protect recovery, be smart about alcohol, and know when NOT to run.")
    return {
        "intro": intro,
        "sections": [
            {"title": "Daily diet · fuel the work", "headers": ["Topic", "Detail"], "rows": FUEL_DIET},
            {"title": "Before running · what & when", "headers": ["Topic", "Detail"], "rows": FUEL_PRE},
            {"title": "During & after · refuel & recover", "headers": ["Topic", "Detail"], "rows": FUEL_POST},
            {"title": "Alcohol · the honest version", "headers": ["Topic", "Detail"], "rows": FUEL_ALC},
            {"title": "Should I run today? · quick guide", "headers": ["Situation", "What to do"], "rows": decide},
        ],
    }


TIPS_COMMON = [
    ["Easy means EASY", "Most running should be conversational — even slower than feels 'proper'. That's where the engine is built."],
    ["The niggle rule", "Pain that changes your gait or worsens = stop. 2–3 easy/off days early beats 3 weeks off later."],
    ["Guard the long run", "The single most important marathon session — the last thing to sacrifice when the week gets messy."],
    ["Sleep is the #1 recovery tool", "7–9 h/night. Higher volume needs more recovery, not less."],
    ["Fuel the long ones", "Past 90 min take 40–60 g carbs/hr and rehearse your race-day breakfast on long runs."],
    ["Rotate 2 pairs of shoes", "Cuts injury risk, extends shoe life (~500–800 km). Buy race shoes by the tune-up and run 3–4 sessions in them."],
    ["Warm up the hard day", "10–15 min easy + a few strides before any tempo/threshold/VO2 work."],
    ["Respect cut-back weeks", "The down weeks are when fitness consolidates — don't 'top them up'."],
    ["Calibrate at the half", "The tune-up half sets your real race pace. Race the pace you EARNED, not the dream."],
    ["Start the race easy", "First few km should feel too easy. Hold back — the marathon starts at 30 km. Even pacing wins."],
    ["Race-day fuel clock", "Gel every 30–40 min from ~45 min in, with water. Don't wait until you're empty."],
    ["Tokyo in early March", "~8–12°C, flat, fast — a great course. Dress for ~+10°C warmer than standing; throwaway layer at the start."],
    ["Nothing new two weeks out", "No new shoes, foods or bonus sessions. Lock the routine and trust the work."],
    ["Log everything", "Fill it in after each run — it keeps you honest and shows patterns before they become problems."],
]
