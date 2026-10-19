"""Jamie's plan (target 4:00, floor 4:30) as structured data. build() -> plan dict.

Weeks 13-33 rebuilt 14 Oct 2026 off actual training -- see the VOL/LR comment below.
"""
from datetime import date, timedelta
import content as C

ID, NAME, GOAL = "jamie", "Jamie", "4:00 (floor 4:30)"
START = date(2026, 7, 20)
RACE  = date(2027, 3, 7)

# Weeks 1–12 are the historical record and are left exactly as first planned, so the
# dashboard keeps showing what was actually asked for against what was actually run.
#
# Weeks 13–33 were REBUILT on 14 Oct 2026 off Jamie's real training, not the original
# ramp. Weeks 7–12 averaged 13.7 km/week and his longest run in seven weeks was 15.7 km
# (11 Oct, 7:36/km @ 159 bpm — slower and +11 bpm against 21.1 km @ 6:24 @ 148 bpm on
# 30 Aug, i.e. detrained, not just under-volumed). The original plan wanted 74 km and a
# 30 km long run in week 13: 5.4x his recent weekly average and 1.9x his longest recent
# run. Week 13 was then re-based to 40 km on 14 Oct, at Jamie's own word that he could
# do 40 this week (he had 9 km banked by the Tuesday). That starting point is the whole
# reason this ramp works: 40 -> 80 km over 16 build weeks is 2x with a cut-back every
# fourth, and no step bigger than 10%, where 30 -> 80 needed steps up to 16%.
#
# What the 40 does NOT change is the long run. His longest run in seven weeks is
# 15.7 km, so Sunday goes to 16 km and the extra weekly volume lands midweek instead
# (Wed/Sat reach 10-12 km at peak). Frequency is the safe way to carry 80 km; a Sunday
# that outruns his proven distance is not. Peak 80 km / 32 km long run (original: 82 / 34).
#
# The standing risk is unchanged and is not about any single week: weeks 7-12 averaged
# 13.7 km. A 40 km week 13 only matters if week 14 is also 44.
VOL = [28,34,40,32,46,52,42,56,
       60,66,54,70,
       40,44,48,42,52,56,46,50,
       50,60,64,54,70,74,60,76,80,74,
       56,40,65]
LR  = [12,14,16,13,18,20,16,22,
       24,26,20,28,
       16,18,20,14,22,24,16,16,
       21.1,26,28,20,30,30,24,30,32,32,
       24,16,42.195]

# Hard (MP-work) long-run weekends — always followed by an easy long-run weekend.
# Documentation only; build_week() reads the session text from sun(), not this set.
HARD_LR = {23, 26, 30}
# Saturday time-trial / checkpoint weeks. sat() supplies the session and its fixed
# distance; build_week() has to know too, or the TT km get double-counted in the pool.
# Wk 10's 5K was planned and missed; wk 16 is the replacement re-anchoring trial.
TT_WEEKS = {10, 16}
# Weeks that run 5 days with Saturday rest (same shape as weeks 1–8). Only wk 13, and
# only because it was already half gone when the plan was rebuilt on the Wednesday —
# its 40 km has to fit into Thu-Sun, so the week is compressed rather than spread.
REBUILD_WEEKS = {13}
# Weeks cut back to only the listed days, everything else turned into rest. Unlike
# OFF_WEEKS this keeps the named sessions at full distance — it's for a week where the
# midweek running has to go but the long run and one supporting run stay. The week's
# target_km follows the days that survive rather than the VOL array, or the dashboard
# would show the week under-target against volume that was deliberately removed.
KEEP_ONLY = {8: ("Fri", "Sun")}
# Individual days rewritten wholesale, applied after the week is otherwise built. Race
# week is the only user: the generator's pool logic cannot know that the 6 days before a
# marathon are not a place to put 13 km on the Wednesday and 10 km on the Saturday.
DAY_OVERRIDE = {33: {"Tue": ("Easy 8 km + 4×100 m strides", "easy", 8),
                     "Wed": ("Easy 6 km — last real run, stay relaxed", "easy", 6),
                     "Thu": ("Easy 5 km + 4×100 m strides", "easy", 5),
                     "Fri": ("Rest", "rest", 0),
                     "Sat": ("Shakeout: easy 4 km + 4×100 m strides", "easy", 4)}}

def phase(w):
    if w<=12: return "Base (interrupted)"
    if w<=16: return "Rebuild / Re-entry"
    if w<=20: return "Aerobic Base"
    if w<=30: return "Marathon-Specific"
    return "Taper & Race"

def tue(w):
    if w<=3:  return "Easy 5–6 km + 4×20s strides", "easy"
    if w<=6:  return "Easy 6–7 km + 6×20s strides", "easy"
    if w<=8:  return "Easy 7 km + 6×20s strides + 4×30s hills", "easy"
    if w<=12:
        lib=["Tempo: 2×10 min @ T, 2 min jog","Easy 8 km + 6×20s strides + 4×30s hills",
             "Threshold: 4×5 min @ T, 90s jog","Cruise: 5×3 min @ T, 75s jog","Tempo: 20 min continuous @ T"]
        s=lib[(w-9)%len(lib)]; return s, ("easy" if "Easy" in s else "quality")
    # Rebuild: no threshold work until there's a base under it. Strides and hills keep
    # some speed in the legs without adding a second hard day to a 30-38 km week.
    if w<=16:
        return {13:"Easy 8 km + 4×20s strides",
                14:"Easy 8 km + 6×20s strides",
                15:"Easy 8 km + 6×20s strides + 4×30s hills",
                16:"Easy 8 km + 4×20s strides (5K trial Saturday — stay fresh)"}[w], "easy"
    if w<=20:
        lib=["Tempo: 2×10 min @ T, 2 min jog","Threshold: 4×5 min @ T, 90s jog",
             "Cruise: 5×3 min @ T, 75s jog","Tempo: 20 min continuous @ T"]
        return lib[(w-17)%len(lib)], "quality"
    # Wk 22 Tuesday is two days after Sevilla — no quality, whatever the library says.
    if w==22: return "Easy 10 km + strides (2 days after Sevilla — nothing hard this week)", "easy"
    if w<=30:
        lib=["Threshold: 4×6 min @ T, 90s jog","MP reps: 5×1.5 km @ MP, 90s jog",
             "Tempo: 2×15 min @ T, 3 min jog","5K reps: 5×1 km @ 5K pace, 90s jog","MP: 6×1 km @ MP, 60s jog"]
        return lib[(w-21)%len(lib)], "quality"
    return {31:"Threshold: 3×5 min @ T, 90s jog",32:"Easy 6 km + 4×20s strides",
            33:"Easy 5 km + 4×100 m strides"}[w], ("quality" if w==31 else "easy")

def thu(w):
    if w<=8:  return ("Easy 5–6 km" if w<=4 else "Easy 6 km + strides"), "easy"
    if w<=12: return ("Easy 8 km + strides" if w%2 else "Easy 8–9 km"), "easy"
    if w<=16: return ("Easy 7 km + strides" if w%2 else "Easy 7 km"), "easy"
    if w<=20: return ("Easy 8 km + strides" if w%2 else "Easy 8 km"), "easy"
    if w<=30:
        # MP tempo only on easy-long-run weeks (never race-adjacent) — max 2 hard efforts/week
        if w==22: return "Easy 10 km — 4 days post-Sevilla", "easy"
        # distance via qkm so the text can't drift from target_km when a week overrides it
        return (("MP tempo: 10 km w/ middle 6 km @ MP","quality") if w in (23,25,29)
                else (f"Easy {qkm(w,'thu')} km","easy"))
    return ({31:"MP: 2×3 km @ MP, 3 min jog",32:"Easy 6 km + strides",33:"Rest or easy 4 km"}[w],
            "quality" if w==31 else "easy")

def sun(w):
    d=LR[w-1]
    txt={13:"16 km easy — RESET: this replaces the 30 km that was planned here. You said "
            "40 km this week, so the volume is there — but your longest run in seven weeks is "
            "15.7 km, so Sunday matches that and the extra km go midweek, not onto this run.",
        16:"14 km easy (cut-back — 5K trial yesterday, keep this one genuinely slow)",
        20:"16 km easy — keep it genuinely easy (Sevilla Half next Sunday)",
        21:"Sevilla Half Marathon — run it CONTROLLED, no faster than long-run pace. "
           "NOT a goal test: it lands 8 weeks into a rebuild and will read slow.",
        22:"26 km easy (post-race — keep it genuinely easy, no MP)",
        23:"28 km, last 6 km @ MP",
        24:"20 km easy (cut-back / festive week — no MP)",
        26:"30 km, last 8 km @ MP",
        27:"TUNE-UP: Half-marathon race (all-out — THIS sets your goal) + w/u & c/d",
        28:"30 km easy (post-race recovery — no MP)",
        29:"32 km easy — keep it genuinely easy (dress rehearsal next weekend)",
        30:"32 km, last 10 km @ MP (final long — dress rehearsal)",
        31:"24 km easy",32:"16 km easy w/ 4×1 km @ MP",
        33:"RACE DAY — Tokyo Marathon · goal set by your build (target 4:00 · floor 4:30)"}
    t = txt.get(w, f"{d:g} km easy" + (" + last 4 km @ MP" if w in (9,12,18) else ""))
    return t, ("race" if w in (21,27,33) else "long")

def sat(w):
    if w==10: return "parkrun 5K — TIME TRIAL (checkpoint) + w/u", "tt", 8
    # Re-anchoring trial: the wk-10 5K never happened, so every pace in this plan is
    # currently an estimate. This one sets them.
    if w==16: return "parkrun 5K — TIME TRIAL (re-anchors every pace below) + w/u", "tt", 8
    if w==33: return "Shakeout: easy 4 km + 4×100 m strides", "easy", 4
    return None, "easy", None

def qkm(w, which):
    if w<=8:  return {"tue":6,"thu":5}[which]
    if w<=12: return {"tue":9,"thu":8}[which]
    if w<=16: return {"tue":8,"thu":7}[which]
    if w<=20: return {"tue":9,"thu":8}[which]
    if w==21: return {"tue":9,"thu":7}[which]
    if w<=30: return {"tue":10,"thu":10}[which]
    # Wk 31 still carries real work — 3x5 min @ T and 2x3 km @ MP — and 6 km days left
    # no room for it, never mind a warm-up. Taper cuts volume, not the session.
    if w==31: return {"tue":8,"thu":10}[which]
    return {"tue":6,"thu":6}[which]

def build_week(w):
    v=VOL[w-1]; lr=LR[w-1]; early=w<=8 or w in REBUILD_WEEKS
    tue_txt,tue_type=tue(w); thu_txt,thu_type=thu(w); sun_txt,sun_type=sun(w)
    sat_txt,sat_type,sat_fixed=sat(w)
    days={}
    days["Mon"]=("Rest / mobility (see S&C)" if w!=33 else "Rest","rest",0)
    tue_km=qkm(w,"tue"); thu_km=qkm(w,"thu")
    tue_txt = C.note_wu(tue_txt, tue_type, tue_km, jog_s=420)
    thu_txt = C.note_wu(thu_txt, thu_type, thu_km, jog_s=420)
    if 5<=w<=30: tue_txt+="  +S&C (hard-day session)"
    known=lr+tue_km+thu_km+((sat_fixed or 0) if w in TT_WEEKS else 0)
    if w==33: known=0
    pool=max(v-known,0)
    if early:
        wed_km=round(pool*0.55); fri_km=max(pool-wed_km,0); sat_km=0
        # A rebuild week's pool is small enough that a 55/45 split produces two
        # pointless 2 km runs. Under ~7 km of filler, give it all to Wednesday and
        # rest Friday — one honest easy run beats two token ones.
        if w in REBUILD_WEEKS and pool<7:
            wed_km=pool; fri_km=0
        fri_txt,fri_type,fri_kmv=(("Rest","rest",0) if (w in REBUILD_WEEKS and fri_km==0)
                                  else (f"Easy {fri_km} km","easy",fri_km))
    else:
        fri_km=round(pool*0.22); wed_km=round(pool*0.42); sat_km=max(pool-fri_km-wed_km,0)
        # Day before a time trial is a rest day, not a 1 km shuffle — its km go to Wed.
        # Only for the rebuilt checkpoints; wk 10 is history and stays as it was.
        if w in TT_WEEKS and w>=13:
            wed_km=pool; fri_km=0; sat_km=0
        sat_km=round(sat_km,1)
        if w in TT_WEEKS and w>=13:
            fri_txt,fri_type,fri_kmv="Rest (day before the trial)","rest",0
        elif w<=30:
            fri_txt=f"Recovery {fri_km} km easy  +S&C (easy-day session)"; fri_type="recovery"; fri_kmv=fri_km
        else:
            # fri_km, not a hardcoded 5: the pool above was already split using fri_km,
            # so a literal here silently pushed the taper weeks over their own target.
            fri_txt="Rest" if w==33 else f"Recovery {fri_km} km easy"
            fri_type="rest" if w==33 else "recovery"; fri_kmv=0 if w==33 else fri_km
    wed_txt=f"Easy {wed_km} km"+("" if early else " + strides")
    if early:
        sat_txt,sat_type,sat_kmv="Rest","rest",0
    elif sat_txt is None:
        sat_txt=f"Easy {sat_km:g} km + strides"; sat_kmv=sat_km
    else:
        sat_kmv=sat_fixed if sat_fixed else sat_km
    days["Tue"]=(tue_txt,tue_type,tue_km); days["Wed"]=(wed_txt,"easy",wed_km)
    days["Thu"]=(thu_txt,thu_type,thu_km); days["Fri"]=(fri_txt,fri_type,fri_kmv)
    days["Sat"]=(sat_txt,sat_type,sat_kmv); days["Sun"]=(sun_txt,sun_type,round(lr,1))
    for dow,spec in DAY_OVERRIDE.get(w,{}).items():
        days[dow]=spec
    keep=KEEP_ONLY.get(w)
    if keep:
        # Days that were already rest keep their own wording (Monday's mobility note);
        # only actual sessions get cleared, so the week still reads as a plan.
        for d in DOW:
            if d not in keep and days[d][1]!="rest":
                days[d]=("Rest","rest",0)
    return days

def focus(w):
    return {10:"5K checkpoint (missed)",13:"RESET — rebuild starts here",
            16:"5K checkpoint (re-anchors paces)",20:"Sevilla is next Sunday",21:"Sevilla Half — controlled",
            27:"Half tune-up (sets your goal)",30:"Final long run",
            33:"RACE WEEK"}.get(w, "Cut-back / recovery week" if w in (4,11,19,24,31) else "")

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
            "note": "Sessions say '@ MP' and '@ T' on purpose — run them at your goal pace: 4:00 = 5:41/km. "
                    "Every pace in this table is currently an ESTIMATE — the wk-10 5K never happened, so nothing "
                    "here is anchored to a real effort. The wk-16 parkrun (Sat 7 Nov) sets them properly; treat "
                    "these as provisional until then."},
        "goals": {"headers": ["Goal", "Marathon pace /km", "/mile", "Half split"], "rows": [
            ["Floor — 4:30", "6:24", "10:18", "2:09:30"],
            ["Target — 4:00", "5:41", "9:09", "1:55:00"],
            ["Stretch — 3:30", "4:59", "8:01", "1:40:45"]]},
        "checkpoints": {
            "intro": "Plan rebuilt 14 Oct (wk 13) off actual training, not the original ramp — weeks 7–12 "
                     "averaged 13.7 km. The 4:00 target is HELD, which is the ambitious read of the data: it "
                     "needs the 80 km peak, and that needs weeks like 7–12 to not happen again. Wk 16 re-anchors "
                     "your paces; the Wk-27 half sets the final race goal (4:00 needs ~1:55).",
            "headers": ["Wk / date", "Test", "Floor 4:30", "Target 4:00", "Stretch 3:30"], "rows": [
                ["Wk 10 · 21 Sep", "5K time trial", "— missed —", "— missed —", "— missed —"],
                ["Wk 16 · Sat 7 Nov", "5K time trial (re-anchor)", "~28:00", "~25:00", "~21:55"],
                ["Wk 21 · Sun 13 Dec", "Sevilla Half — controlled, NOT a test", "—", "—", "—"],
                ["Wk 27 · Sun 24 Jan", "Half-marathon (all-out)", "~2:09:30", "~1:55:00", "~1:40:45"],
                ["Race · 7 Mar", "Marathon", "4:30 · 6:24/km", "4:00 · 5:41/km", "3:30 · 4:59/km"]],
            "notes": [
                "WHY THIS CHANGED: weeks 7–12 averaged 13.7 km/week and the longest run in seven weeks was "
                "15.7 km. Worse, that 11 Oct run was 7:36/km at 159 bpm against 21.1 km at 6:24/km and 148 bpm "
                "on 30 Aug — slower and higher-HR over a shorter distance, which is detraining, not a bad day. "
                "The original wk-13 ask (74 km, 30 km long run) was 5.4x the recent weekly average and 1.9x the "
                "longest recent run. Weeks 1–12 are left untouched as the record; 13 onward is rebuilt.",
                "The rebuild restarts at 40 km — your own number — with a 16 km long run, ramps no more than 10% off the last comparable week, "
                "and cuts back every fourth week. Peak 80 km at wk 29 / 32 km long run. Final long run is "
                "Sun 14 Feb, three weeks out.",
                "3:30 is kept in the table for reference only — it is not a live target after a 12-week start "
                "that produced ~165 km of running. Chasing it is how weeks 9–12 happened.",
                "Football & other sport count as training load — see the banner above. Don't double up hard efforts or stack three hard days.",
                "Max 2 hard run-efforts per week: Tue quality plus EITHER the Thu MP tempo OR a Sunday MP long run — never both. Hard long-run weekends always alternate with easy ones (and football still counts on top).",
                "Rest days are Monday (always), plus Saturday through week 8 and again in the wk 13–15 rebuild; race-week Friday rest is the one exception.",
                "The 80 km peak is load-bearing, not optional — but be clear what it is for. Sub-4 is 5:41/km "
                "and is regularly run off 50–60 km weeks; it is a pace problem more than a volume problem. The "
                "80 km is there to make 4:00 comfortable rather than possible. So if it starts costing you "
                "weeks, drop to ~60 km and keep the consistency: 16 straight weeks at 60 beats 8 at 80 and 8 at "
                "zero, and the second pattern is what weeks 7–12 already were. Make that call at the Wk-27 half, "
                "deliberately, not by quietly missing Sundays.",
                "Sevilla Half (Sun 13 Dec, Wk 21) — signed up alongside Cav. It arrives only 7 weeks into the "
                "rebuild, so it is a controlled long run at long-run pace, NOT a goal test. Running it hard will "
                "produce a number that scares you for no reason. The real test is the Wk-27 half on 24 Jan."]},
        "strength": C.strength("1–20", "21–30", football=True),
        "fuel": C.fuel(football=True, volume_note="it matters a great deal more on the climb to 80 km weeks + football"),
        "research": C.RESEARCH_NOTES,
        "tips": [
            ["Consistency beats any single week", "Weeks 7–12 averaged 13.7 km and cost you real fitness — the 11 Oct long run was slower at a higher heart rate than the one six weeks earlier. Four steady 40 km weeks are worth far more than one 80 km week followed by nothing."],
            ["Volume is the big lever", "Weekly mileage moves your marathon time more than anything — that's why the rebuilt peak is 80 km. But it only counts if you stay healthy and consistent, and it has to be arrived at, not jumped to — 30 km now, 80 km in sixteen weeks, with every fourth week cut back."],
            ["Easy means easy", "Your recent short runs have crept to 5:17–5:54/km while the long runs got slower. That's backwards. The base portions are 6:15–7:00/km; run them there and the long runs come good."],
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
        # A KEEP_ONLY week's volume is whatever the surviving days add up to; using VOL
        # would flag it under-target against km that were deliberately taken out.
        vol=sum(d["target_km"] for d in days) if w in KEEP_ONLY else VOL[w-1]
        weeks.append({"week":w,"start":monday.isoformat(),"phase":phase(w),
                      "target_km":vol,"focus":focus(w),"days":days})
    return {"meta":{"id":ID,"name":NAME,"goal":GOAL,"mp_per_km":"5:41","mp_per_mile":"9:09",
                    "start":START.isoformat(),"race":RACE.isoformat(),
                    "peak_km":max(VOL),"total_weeks":33,
                    "goal_note":"MP = goal pace 4:00 (5:41/km). Plan rebuilt at wk 13 (14 Oct) off actual "
                                "training — weeks 1–12 are left as the record, 13–33 restart from a 30 km week. "
                                "Paces are provisional until the wk-16 5K trial re-anchors them. Football counts "
                                "as a hard session — shuffle runs around matches."},
            "weeks":weeks, "content":content()}
