"""Jamie's plan (target 4:00, reaching 3:30) as structured data. build() -> plan dict."""
from datetime import date, timedelta
import content as C

ID, NAME, GOAL = "jamie", "Jamie", "4:00 (reach 3:30)"
START = date(2026, 7, 20)
RACE  = date(2027, 3, 7)

VOL = [28,34,40,32,46,52,42,56,
       60,66,54,70,74,62,72,76,64,72,
       68,78,82,70,80,66,78,82,72,80,70,60,
       52,40,30]
LR  = [12,14,16,13,18,20,16,22,
       24,26,20,28,30,24,30,32,26,32,
       26,30,32,26,32,21,32,34,28,34,29,24,
       20,16,42.195]

# Hard (MP-work) long-run weekends — always followed by an easy long-run weekend.
HARD_LR = {19, 21, 24, 26, 28, 30}

def phase(w):
    if w<=8:  return "Re-entry / Base"
    if w<=18: return "Aerobic Base"
    if w<=30: return "Marathon-Specific"
    return "Taper & Race"

def tue(w):
    if w<=3:  return "Easy 5–6 km + 4×20s strides", "easy"
    if w<=6:  return "Easy 6–7 km + 6×20s strides", "easy"
    if w<=8:  return "Easy 7 km + 6×20s strides + 4×30s hills", "easy"
    if w<=18:
        lib=["Tempo: 2×10 min @ T, 2 min jog","Easy 8 km + 6×20s strides + 4×30s hills",
             "Threshold: 4×5 min @ T, 90s jog","Cruise: 5×3 min @ T, 75s jog","Tempo: 20 min continuous @ T"]
        s=lib[(w-9)%len(lib)]; return s, ("easy" if "Easy" in s else "quality")
    if w<=30:
        lib=["Threshold: 4×6 min @ T, 90s jog","MP reps: 5×1.5 km @ MP, 90s jog",
             "Tempo: 2×15 min @ T, 3 min jog","5K reps: 5×1 km @ 5K pace, 90s jog","MP: 6×1 km @ MP, 60s jog"]
        return lib[(w-19)%len(lib)], "quality"
    return {31:"Threshold: 3×5 min @ T, 90s jog",32:"Easy 5 km + 4×20s strides",
            33:"Easy 5 km + 4×100 m strides"}[w], ("quality" if w==31 else "easy")

def thu(w):
    if w<=8:  return ("Easy 5–6 km" if w<=4 else "Easy 6 km + strides"), "easy"
    if w<=18: return ("Easy 8 km + strides" if w%2 else "Easy 8–9 km"), "easy"
    if w<=30:
        # MP tempo only on easy-long-run weeks (never race-adjacent) — max 2 hard efforts/week
        return (("MP tempo: 11 km w/ middle 6 km @ MP","quality") if w in (20,22,27,29)
                else ("Easy 9 km","easy"))
    return ({31:"MP: 2×3 km @ MP, 3 min jog",32:"Easy 6 km + strides",33:"Rest or easy 4 km"}[w],
            "quality" if w==31 else "easy")

def sun(w):
    d=LR[w-1]
    txt={19:"26 km, last 6 km @ MP",
        20:"30 km easy (recovery weekend — no MP)",
        21:"32 km, last 8 km @ MP",
        23:"32 km easy — keep it genuinely easy (half race next weekend)",
        24:"TUNE-UP: Half-marathon race (all-out — this sets your goal) + w/u & c/d",
        25:"32 km easy (post-race recovery — no MP)",
        26:"34 km, last 10 km @ MP",
        28:"34 km, last 12 km @ MP (final long — dress rehearsal)",
        29:"29 km easy (recovery weekend — no MP)",
        30:"24 km, last 6 km @ MP",
        31:"20 km easy",32:"16 km easy w/ 4×1 km @ MP",
        33:"RACE DAY — Tokyo Marathon · goal set by your build (4:00 · floor 4:30 · reach 3:30)"}
    t = txt.get(w, f"{d:g} km easy" + (" + last 4 km @ MP" if w in (9,12,15) else ""))
    return t, ("race" if w in (24,33) else "long")

def sat(w):
    if w==10: return "parkrun 5K — TIME TRIAL (checkpoint) + w/u", "tt", 8
    if w==18: return "10K TIME TRIAL or local race (checkpoint) + w/u", "tt", 12
    if w==33: return "Shakeout: easy 4 km + 4×100 m strides", "easy", 4
    return None, "easy", None

def qkm(w, which):
    if w<=8:  return {"tue":6,"thu":5}[which]
    if w<=18: return {"tue":9,"thu":8}[which]
    if w<=30: return {"tue":10,"thu":10}[which]
    return {"tue":6,"thu":6}[which]

def build_week(w):
    v=VOL[w-1]; lr=LR[w-1]; early=w<=8
    tue_txt,tue_type=tue(w); thu_txt,thu_type=thu(w); sun_txt,sun_type=sun(w)
    sat_txt,sat_type,sat_fixed=sat(w)
    days={}
    days["Mon"]=("Rest / mobility (see S&C)" if w!=33 else "Rest","rest",0)
    tue_km=qkm(w,"tue"); thu_km=qkm(w,"thu")
    if 5<=w<=30: tue_txt+="  +S&C A"
    known=lr+tue_km+thu_km+((sat_fixed or 0) if w in (10,18) else 0)
    if w==33: known=0
    pool=max(v-known,0)
    if early:
        wed_km=round(pool*0.55); fri_km=max(pool-wed_km,0); sat_km=0
        fri_txt,fri_type,fri_kmv=f"Easy {fri_km} km","easy",fri_km
    else:
        fri_km=round(pool*0.22); wed_km=round(pool*0.42); sat_km=max(pool-fri_km-wed_km,0)
        if w<=30:
            fri_txt=f"Recovery {fri_km} km easy  +S&C B"; fri_type="recovery"; fri_kmv=fri_km
        else:
            fri_txt="Rest" if w==33 else "Recovery 5 km easy"
            fri_type="rest" if w==33 else "recovery"; fri_kmv=0 if w==33 else 5
    wed_txt=f"Easy {wed_km} km"+("" if early else " + strides")
    if early:
        sat_txt,sat_type,sat_kmv="Rest","rest",0
    elif sat_txt is None:
        sat_txt=f"Easy {sat_km} km + strides"; sat_kmv=sat_km
    else:
        sat_kmv=sat_fixed if sat_fixed else sat_km
    days["Tue"]=(tue_txt,tue_type,tue_km); days["Wed"]=(wed_txt,"easy",wed_km)
    days["Thu"]=(thu_txt,thu_type,thu_km); days["Fri"]=(fri_txt,fri_type,fri_kmv)
    days["Sat"]=(sat_txt,sat_type,sat_kmv); days["Sun"]=(sun_txt,sun_type,round(lr,1))
    return days

def focus(w):
    return {10:"5K checkpoint",18:"10K checkpoint",24:"Half tune-up (sets your goal)",
            28:"Final long run",33:"RACE WEEK"}.get(w, "Cut-back / recovery week" if w in (4,11,14,17,22,27) else "")

DOW=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

def content():
    return {
        "banner": ("⚽ Football = a hard session. If a match falls on a Tue or Sat: don't also do a hard run "
                   "that day — move the quality run to the next easy day, or let football BE that week's hard "
                   "session and keep the runs easy. Never stack quality run + football + long run on 3 straight "
                   "days; keep the day after a match easy. Max ~2 hard efforts/week (football counts) + the long run."),
        "paces": {"headers": ["Zone", "per km", "per mile", "Use"], "rows": [
            ["Recovery", "6:45–7:20", "10:52–11:48", "Easy/short & day-after runs"],
            ["Easy / aerobic", "6:15–7:00", "10:03–11:16", "Bulk of running — keep it TRULY easy"],
            ["Long-run easy", "6:20–7:00", "10:11–11:16", "Long-run base portions"],
            ["Marathon (MP) — 4:00", "5:41", "9:09", "Race pace — MP blocks & long-run finishes"],
            ["Threshold (T)", "5:15–5:25", "8:27–8:43", "Tempo / cruise (comfortably hard)"],
            ["5K pace", "4:55–5:05", "7:55–8:09", "Short faster reps"],
            ["Strides", "relaxed-fast", "—", "20s pickups, not a workout"]],
            "note": "Sessions say '@ MP' and '@ T' on purpose — run them at your CURRENT goal pace. Start at 4:00 "
                    "(5:41/km); as checkpoints come in faster, shift MP toward 3:30 (4:59/km) and pull threshold with it."},
        "goals": {"headers": ["Goal", "Marathon pace /km", "/mile", "Half split"], "rows": [
            ["Floor — 4:30", "6:24", "10:18", "2:09:30"],
            ["Target — 4:00", "5:41", "9:09", "1:55:00"],
            ["Reach — 3:30", "4:59", "8:01", "1:40:45"]]},
        "checkpoints": {
            "intro": "Run these honestly and set your race goal off the data. The Wk-24 half is the big one — "
                     "3:30 needs your half near 1:41; 4:00 needs ~1:55.",
            "headers": ["Wk / date", "Test", "Floor 4:30", "Target 4:00", "Reach 3:30"], "rows": [
                ["Wk 10 · ~21 Sep", "5K time trial", "~28:00", "~25:00", "~21:55"],
                ["Wk 18 · ~16 Nov", "10K time trial", "~58:30", "~52:10", "~45:40"],
                ["Wk 24 · ~28 Dec", "Half-marathon", "~2:09:30", "~1:55:00", "~1:40:45"],
                ["Race · 7 Mar", "Marathon", "4:30 · 6:24/km", "4:00 · 5:41/km", "3:30 · 4:59/km"]],
            "notes": [
                "This build pushes volume (peak ~82 km) so 3:30 stays achievable — volume is the biggest lever for marathon time.",
                "Football & other sport count as training load — see the banner above. Don't double up hard efforts or stack three hard days.",
                "Max 2 hard run-efforts per week: Tue quality plus EITHER the Thu MP tempo OR a Sunday MP long run — never both. Hard long-run weekends always alternate with easy ones (and football still counts on top).",
                "Rest days are Monday (always) and Saturday through week 8; race-week Friday rest is the one exception.",
                "If 82 km proves too much with football, ~68 km still delivers a strong 4:00."]},
        "strength": C.strength("1–18", "19–30", football=True),
        "fuel": C.fuel(football=True, volume_note="it matters more with 80 km weeks + football"),
        "research": C.RESEARCH_NOTES,
        "tips": [
            ["Volume is the big lever", "Weekly mileage moves your marathon time more than anything — that's why the peak is ~82 km. But it only counts if you stay healthy and consistent."],
            ["Football is a hard session", "Treat every match as one of your two weekly hard efforts. No hard run the same day; keep the day after a match easy."],
            ["Shuffle, don't skip", "Match Tuesday? Move the quality run to Wednesday and slide the easy days along. Match Saturday? Keep Sunday's long run easy, or push it to Monday if legs are cooked. Protect the long run; don't stack three hard days."],
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
    return {"meta":{"id":ID,"name":NAME,"goal":GOAL,"mp_per_km":"5:41","mp_per_mile":"9:09",
                    "start":START.isoformat(),"race":RACE.isoformat(),
                    "peak_km":max(VOL),"total_weeks":33,
                    "goal_note":"MP = current goal pace: start 4:00 (5:41/km), shift toward 3:30 (4:59/km) "
                                "as checkpoints allow. Football counts as a hard session — shuffle runs around matches."},
            "weeks":weeks, "content":content()}
