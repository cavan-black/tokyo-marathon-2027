"""Cav's sub-2:50 plan as structured data. build() -> plan dict."""
from datetime import date, timedelta
import content as C

ID, NAME, GOAL = "cav", "Cav", "2:50:00"
START = date(2026, 7, 20)
RACE  = date(2027, 3, 7)

VOL = [42,50,56,48,
       62,70,76,66,82,88,74,92,96,
       80,100,106,90,108,112,92,108,116,98,
       112,118,102,116,110,106,90,
       74,56,38]
LR  = [12,14,16,14,
       18,20,22,18,24,26,22,28,30,
       24,28,30,26,32,32,21,32,34,28,
       32,34,28,34,32,35,30,
       26,18,42.195]

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
        lib=["Threshold: 6×1.5 km @ 3:48/km, 60s jog","Race reps: 5×1 mile @ 3:52/km, 90s jog",
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
    return {31:"MP: 2×3 km @ 4:01/km, 3 min jog",32:"Easy 8 km + 6×20s strides",33:"Rest or easy 5 km"}[w], "easy"

def sun(w):
    d=LR[w-1]
    txt={16:"30 km, last 8 km @ MP",18:"32 km, last 10 km @ MP",
        19:"32 km w/ 3×5 km @ MP in 2nd half",20:"TUNE-UP: Half-marathon race (all-out) + w/u & c/d",
        21:"32 km, last 12 km @ MP",22:"34 km, last 12 km @ MP",
        24:"32 km w/ 2×10 km @ MP",25:"34 km, MIDDLE 18 km @ MP (key session)",
        27:"34 km w/ 3×6 km @ MP",28:"32 km, last 14 km @ MP",
        29:"35 km, last 12 km @ MP (dress rehearsal)",30:"30 km steady, last 8 km @ MP — FINAL long run",
        31:"26 km, last 8 km @ MP",32:"18 km easy w/ 4×1 km @ MP",
        33:"RACE DAY — Tokyo Marathon · 2:50 target · 4:01/km · 6:29/mi"}
    t = txt.get(w, f"{d:g} km easy" + (" + last 4 km relaxed @ MP" if 5 <= w <= 13 and w % 3 == 0 else ""))
    return t, ("race" if w in (20,33) else "long")

def sat(w):
    if w == 9:  return "parkrun 5K — TIME TRIAL (fitness check) + w/u & c/d", "tt", 9
    if w == 13: return "10K TIME TRIAL or local race (fitness check) + w/u", "tt", 13
    if w == 26: return "10K / 10-mile sharpener race (optional) + w/u", "tt", 14
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
    known=lr+tue_km+thu_km+((sat_fixed or 0) if w in (9,13,26) else 0)
    if w==33: known=0
    pool=max(v-known,0)
    fri_km=round(pool*0.28); wed_km=round(pool*0.40); sat_km=max(pool-fri_km-wed_km,0)
    wed_txt=f"Easy {wed_km} km"+("" if reentry else " + 6×20s strides")
    fri_txt=("Rest" if (reentry or w==33) else f"Recovery {fri_km} km easy"+("  +light S&C" if 31<=w<=32 else "  +S&C B"))
    fri_type="rest" if (reentry or w==33) else "recovery"
    fri_kmv=0 if fri_type=="rest" else fri_km
    if sat_txt is None:
        sat_txt=f"Easy {sat_km} km"+("" if reentry else " + strides"); sat_kmv=sat_km
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
            20:"Half tune-up (calibrate goal)",26:"Sharpener race + cut-back",
            29:"Peak long run",33:"RACE WEEK"}.get(w, "Cut-back / recovery week" if w in (4,8,11,17,23) else "")

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
            "note": "Run easy days and ALL doubles genuinely easy — conversational. Keep the 3 quality days "
                    "(Tue/Thu/Sun) as the only hard efforts."},
        "checkpoints": {
            "intro": "2:50 is the A-goal; your PRs predict ~3:06–3:27, and this build targets the gap with volume. "
                     "Don't lock race-day pace until the Wk-20 half.",
            "headers": ["Wk / date", "Test", "On-track for 2:50", "If short — likely target"], "rows": [
                ["Wk 9 · ~14 Sep", "5K time trial", "≤ 18:05", "18:05–18:45 → ~2:55-3:00 · >19:00 → 3:05+"],
                ["Wk 13 · ~12 Oct", "10K time trial", "≤ 37:45", "37:45–39:00 → sub-3 · >40:00 → 3:05+"],
                ["Wk 20 · ~30 Nov", "Half-marathon", "≤ 1:23:30", "1:23:30–1:26 → sub-3 · >1:27 → 3:05–3:10"],
                ["Race · 7 Mar", "Marathon", "2:50 = 4:01/km", "Start at CONFIRMED pace. Even splits."]],
            "notes": [
                "Peak ~118 km — weekly volume is the biggest lever for marathon time, and the extra should be EASY miles (your endurance lags your speed).",
                "6 run-days + doubles, Monday kept as a full rest day.",
                "Injury risk is about ramp rate, not the ceiling — ~7–10% weekly steps; respect cut-back weeks (4,8,11,17,23).",
                "If 118 km proves unrealistic, the ~105 km version is still solidly sub-3."]},
        "strength": C.strength("1–13", "14–30", football=False),
        "fuel": C.fuel(football=False, volume_note="it matters more with 100+ km weeks"),
        "tips": [
            ["Volume is the big lever", "Marathon time tracks weekly mileage more than any other trainable factor — that's why the peak is ~118 km. Add it as EASY miles."],
            ["Doubles > longer hard runs", "Two short easy runs add volume with less injury risk than lengthening workouts — that's how you reach ~118 km with a rest day intact."],
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
