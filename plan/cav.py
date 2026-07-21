"""Cav's sub-2:50 plan as structured data. build() -> plan dict."""
from datetime import date, timedelta
import content as C

ID, NAME, GOAL = "cav", "Cav", "2:50:00"
START = date(2026, 7, 20)
RACE  = date(2027, 3, 7)

VOL = [42,50,56,48,
       62,70,76,66,82,88,74,92,96,
       80,100,106,90,108,112,92,104,108,76,
       86,106,112,116,110,106,90,
       74,56,38]
LR  = [12,14,16,14,
       18,20,22,18,24,26,22,28,30,
       24,28,30,26,32,32,21,30,32,20,
       24,30,28,34,32,35,30,
       26,18,42.195]
# Wk 23 (21-27 Dec, Christmas) and Wk 24 (28 Dec-3 Jan, New Year) are a deliberate
# holiday dip after the Wk-20 half; Wk 25 (from Mon 4 Jan, the day after NYD+1)
# resumes the ramp back to peak.

# Hard (MP-work) long-run weekends — always followed by an easy long-run weekend.
HARD_LR = {16, 18, 20, 22, 25, 27, 29, 31}
TT_WEEKS = {9, 13, 26}

def phase(w):
    if w <= 4:  return "Re-entry / Rebuild"
    if w <= 13: return "Aerobic Base"
    if w <= 23: return "Marathon-Specific I"
    if w <= 30: return "Specific II / Peak"
    return "Taper & Race"

def tue(w):
    if w <= 4:   return "Easy 10 km + 6×20s strides", "easy"
    if w <= 13:
        lib=["Threshold: 5×1 km @ 3:50/km (T), 90s jog","Tempo: 2×12 min @ 3:52/km, 3 min jog",
             "Threshold: 6×1 km @ 3:48/km, 75s jog","Tempo: 25 min continuous @ 3:52/km"]
        return lib[(w-5)%len(lib)], "quality"
    if w <= 23:
        lib=["VO2: 5×1000 m @ 3:28/km (I), 2:30 jog","Threshold: 4×2 km @ 3:50/km, 90s jog",
             "VO2: 6×1000 m @ 3:26/km, 2:30 jog","Threshold: 5×1.5 km @ 3:48/km, 75s jog"]
        return lib[(w-14)%len(lib)], "quality"
    if w <= 30:
        lib=["Threshold: 6×1.5 km @ 3:48/km, 60s jog","Race reps: 5×1.6 km @ 3:52/km, 90s jog",
             "Threshold: 3×3 km @ 3:50/km, 2 min jog","VO2/sharpen: 6×800 m @ 3:24/km, 2 min jog"]
        return lib[(w-24)%len(lib)], "quality"
    return {31:"Threshold: 4×1 km @ 3:50/km, 90s jog",32:"Sharpen: 3×1 km @ 3:48/km, 2 min jog",
            33:"Easy 8 km + 4×100 m strides"}[w], ("quality" if w<33 else "easy")

def thu(w):
    if w <= 4:   return "Easy 8 km", "easy"
    if w <= 13:  return ("Hill strides: easy 11 km + 8×15s hill sprints" if w%2 else "Medium easy 12 km + 6×20s strides"), "easy"
    if w <= 23:
        lib=["MP tempo: 2×5 km @ 4:01/km (MP), 3 min float","Medium-long 16 km w/ middle 8 km @ MP",
             "MP tempo: 3×4 km @ MP, 2 min float","Medium-long 16 km easy + 8×15s hill sprints"]
        return lib[(w-14)%len(lib)], "quality"
    if w <= 30:
        lib=["MP: 3×6 km @ 4:01/km, 3 min jog","Medium-long 18 km w/ 10 km @ MP",
             "MP: 2×8 km @ MP, 3 min float","Medium-long 17 km easy"]
        return lib[(w-24)%len(lib)], "quality"
    return {31:"Easy 8 km + 4×20s strides",32:"Easy 8 km + 6×20s strides",33:"Rest or easy 5 km"}[w], "easy"

def sun(w):
    d=LR[w-1]
    txt={16:"30 km, last 8 km @ MP",18:"32 km, last 10 km @ MP",
        19:"32 km easy (recovery weekend — no MP)",
        20:"TUNE-UP: Half-marathon race (all-out) + w/u & c/d",
        21:"30 km easy (post-race — keep it genuinely easy)",
        22:"32 km, last 10 km @ MP",
        23:"20 km easy — Christmas week, keep it light",
        24:"24 km easy — New Year week, ease back in",
        25:"30 km, last 10 km @ MP — ramp resumes",
        26:"28 km easy (recovery weekend — no MP)",
        27:"34 km w/ 3×6 km @ MP",
        28:"32 km easy (recovery weekend — no MP)",
        29:"35 km, last 12 km @ MP (dress rehearsal)",
        30:"30 km easy — FINAL long run, keep it relaxed",
        31:"26 km, last 8 km @ MP",32:"18 km easy w/ 4×1 km @ MP",
        33:"RACE DAY — Tokyo Marathon · 2:50 target · 4:01/km · 6:29/mi"}
    t = txt.get(w, f"{d:g} km easy" + (" + last 4 km relaxed @ MP" if w in (6,12) else ""))
    return t, ("race" if w in (20,33) else "long")

def sat(w):
    if w == 9:  return "parkrun 5K — TIME TRIAL (fitness check) + w/u & c/d", "tt", 9
    if w == 13: return "10K TIME TRIAL or local race (fitness check) + w/u", "tt", 13
    if w == 26: return "10K / 16 km sharpener race (optional) + w/u", "tt", 14
    if w == 33: return "Shakeout: easy 4 km + 4×100 m strides", "easy", 4
    return None, "easy", None

def qkm(w, which):
    if w <= 4:  return {"tue":10,"thu":8}[which]
    if w <= 13: return {"tue":13,"thu":11}[which]
    if w <= 23: return {"tue":14,"thu":16}[which]
    if w <= 30: return {"tue":15,"thu":17}[which]
    return {"tue":9,"thu":8}[which]

def build_week(w):
    v=VOL[w-1]; lr=LR[w-1]; reentry = w<=4
    tue_txt,tue_type = tue(w); thu_txt,thu_type = thu(w); sun_txt,sun_type = sun(w)
    sat_txt,sat_type,sat_fixed = sat(w)
    days={}
    days["Mon"]=("Rest" if (reentry or w==33) else "Rest / mobility (full rest day)","rest",0)
    tue_km=qkm(w,"tue"); thu_km=qkm(w,"thu")
    if 4<=w<=30: tue_txt += "  +S&C A"
    # Max 2 hard days/week: Thu is quality only when Sunday's long run is easy and there's no Sat TT
    hard_sun = sun_type == "race" or w in HARD_LR
    if thu_type == "quality" and (hard_sun or w in TT_WEEKS):
        thu_txt, thu_type = f"Medium-long {thu_km} km easy", "easy"
    known=lr+tue_km+thu_km+((sat_fixed or 0) if w in TT_WEEKS else 0)
    if w==33: known=0
    pool=max(v-known,0)
    if reentry:
        wed_km=round(pool*0.55); fri_km=max(pool-wed_km,0); sat_km=0
    else:
        fri_km=round(pool*0.28); wed_km=round(pool*0.40); sat_km=max(pool-fri_km-wed_km,0)
    wed_txt=f"Easy {wed_km} km"+("" if reentry else " + 6×20s strides")
    if reentry:
        fri_txt,fri_type,fri_kmv=f"Easy {fri_km} km","easy",fri_km
    elif w==33:
        fri_txt,fri_type,fri_kmv="Rest","rest",0
    else:
        fri_txt=f"Recovery {fri_km} km easy"+("  +light S&C" if 31<=w<=32 else "  +S&C B")
        fri_type,fri_kmv="recovery",fri_km
    if reentry:
        sat_txt,sat_type,sat_kmv="Rest","rest",0
    elif sat_txt is None:
        sat_txt=f"Easy {sat_km} km + strides"; sat_kmv=sat_km
    else:
        sat_kmv=sat_fixed if sat_fixed else sat_km
    if 5<=w<=30:
        if v>=98:  wed_txt+="  (double: split AM/PM)"
        if v>=108: sat_txt+="  (double)"
        if v>=114: tue_txt+="  (PM easy double)"
    days["Tue"]=(tue_txt,tue_type,tue_km); days["Wed"]=(wed_txt,"easy",wed_km)
    days["Thu"]=(thu_txt,thu_type,thu_km); days["Fri"]=(fri_txt,fri_type,fri_kmv)
    days["Sat"]=(sat_txt,sat_type,sat_kmv); days["Sun"]=(sun_txt,sun_type,round(lr,1))
    return days

def focus(w):
    return {9:"5K time-trial checkpoint",13:"10K time-trial checkpoint",
            20:"Half tune-up (calibrate goal)",23:"🎄 Christmas week — deliberate holiday dip",
            24:"🎆 New Year week — easing back in",25:"Ramp resumes (from the day after NYD)",
            29:"Peak long run",33:"RACE WEEK"}.get(w, "Cut-back / recovery week" if w in (4,8,11,17) else "")

DOW=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

def content():
    return {
        "paces": {"headers": ["Zone", "per km", "per mile", "Use"], "rows": [
            ["Recovery", "5:35–6:05", "8:59–9:47", "Easy shakeouts, doubles, day-after"],
            ["Easy / aerobic", "5:00–5:35", "8:03–8:59", "Bulk of weekly volume (incl. doubles)"],
            ["Long-run easy", "4:55–5:30", "7:55–8:51", "Long-run base portions"],
            ["Marathon (MP)", "4:01", "6:29", "Race pace — MP blocks & long-run finishes"],
            ["Threshold (T)", "3:45–3:52", "6:02–6:13", "Tempo / cruise intervals (15K–HM effort)"],
            ["10K pace", "3:36", "5:47", "Longer VO2 / race sharpeners"],
            ["Interval (I, 5K)", "3:24–3:32", "5:29–5:41", "VO2 max reps"],
            ["Strides", "~3:10 feel", "relaxed-fast", "20s pickups, not a workout"]],
            "note": "Run easy days and ALL doubles genuinely easy — conversational. Max 2 hard days per week: "
                    "Tue quality plus EITHER the Thu session OR a Sunday MP long run — never both. Hard "
                    "long-run weekends always alternate with easy ones."},
        "checkpoints": {
            "intro": "2:50 is the A-goal; your PRs predict ~3:06–3:27, and this build targets the gap with volume. "
                     "Don't lock race-day pace until the Wk-20 half.",
            "headers": ["Wk / date", "Test", "On-track for 2:50", "If short — likely target"], "rows": [
                ["Wk 9 · ~14 Sep", "5K time trial", "≤ 18:05", "18:05–18:45 → ~2:55-3:00 · >19:00 → 3:05+"],
                ["Wk 13 · ~12 Oct", "10K time trial", "≤ 37:45", "37:45–39:00 → sub-3 · >40:00 → 3:05+"],
                ["Wk 20 · ~30 Nov", "Half-marathon", "≤ 1:23:30", "1:23:30–1:26 → sub-3 · >1:27 → 3:05–3:10"],
                ["Race · 7 Mar", "Marathon", "2:50 = 4:01/km", "Start at CONFIRMED pace. Even splits."]],
            "notes": [
                "Peak ~116 km — weekly volume is the biggest lever for marathon time, and the extra should be EASY km (your endurance lags your speed).",
                "Rest days are Monday (always) and Saturday in the re-entry weeks; race-week Friday rest is the one exception.",
                "Hard long runs alternate with easy ones — never two hard long-run weekends in a row, and the weekends before/after the Wk-20 half are easy.",
                "Wk 23 (Christmas) and Wk 24 (New Year) are a deliberate holiday dip — volume drops to ~76-86 km so the block doesn't fight the festive season. The ramp resumes from Wk 25, the week starting the day after New Year's Day.",
                "Injury risk is about ramp rate, not the ceiling — ~7–10% weekly steps; respect cut-back weeks (4,8,11,17) and the holiday dip (23,24).",
                "If 116 km proves unrealistic, the ~105 km version is still solidly sub-3."]},
        "strength": C.strength("1–13", "14–30", football=False),
        "fuel": C.fuel(football=False, volume_note="it matters more with 100+ km weeks"),
        "research": C.RESEARCH_NOTES,
        "diet": {
            "intro": "Starting at 71 kg, aiming to bank a few kg of surplus before volume climbs into the "
                     "90–116 km/wk range — better to arrive there with some reserve than fight a deficit on "
                     "top of high mileage. A lean, slow surplus so the gain is mostly muscle/glycogen, not "
                     "fat you then have to carry up every long run.",
            "targets": {"headers": ["Metric", "Target", "Why"], "rows": [
                ["Daily surplus", "+300–500 kcal above maintenance",
                 "Slow, controlled gain — a fast surplus is fat gain you carry through 116 km weeks"],
                ["Protein", "1.8–2.2 g/kg (≈130–155 g/day at 71 kg)",
                 "Muscle repair & retention while running volume climbs"],
                ["Carbs", "6–10 g/kg on big days (≈425–710 g)",
                 "Fuels the work AND is what actually makes a surplus achievable at this mileage"],
                ["Rate of gain", "~0.25–0.5 kg/week",
                 "Faster than this risks fat gain with little functional benefit"],
            ]},
            "additions": {"headers": ["Add-in", "Why it earns its place", "Easy way in"], "rows": [
                ["Whole milk", "Cheap calories + protein + calcium, easy to drink in volume",
                 "Big glass with breakfast, in the post-run smoothie, on cereal"],
                ["Banana", "Fast carbs + potassium, hides well in smoothies",
                 "1–2/day — pre-run, in smoothies, with peanut butter"],
                ["Peanut butter", "Very calorie-dense (~190 kcal/tbsp), easy to add anywhere",
                 "Toast, banana, oats, or a spoon straight from the jar post-run"],
                ["Summer fruit (berries, stone fruit)", "Micronutrients + easy extra carbs without a fibre overload",
                 "Snacks, with yoghurt, blended into smoothies"],
                ["Sunflower seeds", "Calorie-dense, healthy fats + magnesium/vitamin E for recovery",
                 "Sprinkle on porridge/salads, handful as a snack"],
                ["Creatine (5 g/day)", "Supports strength work and may aid recovery/lean gain; cheap, well-studied",
                 "5 g daily, any time — doesn't need to be around training"],
                ["Greek yoghurt", "Protein-dense and versatile", "With fruit/granola, or as a smoothie base"],
                ["Olive oil / nut butters", "Dense calories without a huge volume of food",
                 "Drizzle on food, extra spoon in smoothies"],
            ]},
            "smoothie": {
                "title": "Go-to mass-gain smoothie · ~700–800 kcal, ~40 g protein",
                "ingredients": ["300 ml whole milk", "1 banana", "2 tbsp peanut butter",
                                 "1 cup mixed summer fruit / berries", "1 tbsp sunflower seeds",
                                 "1 scoop protein powder (optional)", "5 g creatine",
                                 "Handful of oats (optional — extra carbs + thickness)"],
                "note": "Drink it alongside a meal, not instead of one — a smoothie goes down easily on top "
                        "of normal eating without feeling 'full', which is exactly the point when chasing a surplus.",
            },
            "meals": {"headers": ["Time", "Suggestion"], "rows": [
                ["Wake-up", "Big glass of whole milk + a banana, or straight into breakfast if training early"],
                ["Breakfast", "Porridge made with whole milk, banana, peanut butter, sunflower seeds + honey — "
                              "or eggs on toast with avocado + a glass of milk"],
                ["Mid-morning", "Mass-gain smoothie (see recipe), or Greek yoghurt + granola + summer fruit"],
                ["Lunch", "Big carb base (rice/pasta/potatoes) + protein (chicken/fish/tofu/beans) + veg + olive oil"],
                ["Pre-run (PM sessions)", "Banana + toast + jam, or a small carb-heavy snack 60–90 min before"],
                ["Post-run", "Recovery meal within ~60 min: carbs + 20–30 g protein — a milk-based smoothie, "
                             "or a proper meal if timing allows"],
                ["Dinner", "Protein + carbs + veg — a bigger portion than feels 'normal'; this is where most "
                          "of the surplus should land"],
                ["Before bed", "Greek yoghurt + peanut butter, or a glass of milk + a handful of nuts — "
                               "slow-digesting protein/calories overnight"],
            ]},
            "notes": [
                "Weigh in weekly (same day, same conditions) — trust the 2–3 week trend, not daily noise.",
                "If the scale isn't moving after 2 weeks of genuinely trying, add another 200–300 kcal/day rather than overcorrecting hard.",
                "Once volume gets into the 90+ km/wk range (~Wk 15–16 onward) appetite usually rises on its own — "
                "the surplus gets easier to hit, and the challenge shifts to not falling behind on recovery.",
                "General sports-nutrition guidance, not individualised medical advice — adjust to how your body actually responds.",
            ],
        },
        "tips": [
            ["Volume is the big lever", "Marathon time tracks weekly mileage more than any other trainable factor — that's why the peak is ~116 km. Add it as EASY km."],
            ["Doubles > longer hard runs", "Two short easy runs add volume with less injury risk than lengthening workouts — that's how you reach ~116 km with a rest day intact."],
            ["Ramp is the risk, not the ceiling", "Injuries come from increasing load too fast for your base, not from high mileage itself. ~7–10% weekly steps."],
        ] + C.TIPS_COMMON,
    }


def build():
    weeks=[]
    for w in range(1,34):
        monday=START+timedelta(days=(w-1)*7); dm=build_week(w); days=[]
        for i,dow in enumerate(DOW):
            txt,typ,km=dm[dow]
            days.append({"date":(monday+timedelta(days=i)).isoformat(),"dow":dow,
                         "type":typ,"session":txt,"target_km":km})
        weeks.append({"week":w,"start":monday.isoformat(),"phase":phase(w),
                      "target_km":VOL[w-1],"focus":focus(w),"days":days})
    return {"meta":{"id":ID,"name":NAME,"goal":GOAL,"mp_per_km":"4:01","mp_per_mile":"6:29",
                    "start":START.isoformat(),"race":RACE.isoformat(),
                    "peak_km":max(VOL),"total_weeks":33,
                    "goal_note":"Anchored on 2:50 (4:01/km). Calibrate at the Wk-20 half."},
            "weeks":weeks, "content":content()}
