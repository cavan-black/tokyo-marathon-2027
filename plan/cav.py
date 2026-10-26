"""Cav's sub-2:48 plan as structured data. build() -> plan dict."""
from datetime import date, timedelta
import content as C

ID, NAME, GOAL = "cav", "Cav", "2:48:00"
START = date(2026, 7, 20)
RACE  = date(2027, 3, 7)

# Re-planned 2026-08-20. Weeks 1-4 are history and untouched. Wk 6 is a week off (see
# OFF_WEEKS), and the original ramp — 70/76/66/82/88 through the base phase — assumed a
# ~56 km/wk starting point that never materialised: weeks 1-5 actually ran 42, 29, 70, ~27
# and ~38, a ~40 km/wk chronic load. Rebuilding from where the runner IS rather than where
# the old array assumed he'd be, at 7-11% peak-to-peak steps. Peak is still 116, one week
# later (Wk 28 rather than 27), which is still 5 weeks out from the race.
VOL = [42,50,56,48,
       62,0,45,54,60,50,66,72,64,
       76,84,90,76,97,101,92,80,96,76,
       88,107,99,110,116,110,94,
       69,56,70]
LR  = [12,14,16,14,
       18,0,14,16,18,16,20,22,18,
       24,26,28,24,32,30,28,24,30,20,
       24,32,28,38,32,35,32,
       21,18,42.195]
# Wk 23 (21-27 Dec, Christmas) and Wk 24 (28 Dec-3 Jan, New Year) are a deliberate
# holiday dip after the Wk-21 half; Wk 25 (from Mon 4 Jan, the day after NYD+1)
# resumes the ramp back to peak.

# Hard long-run weekends (MP work, or wk 27's 38 km) — always followed by an easy one.
HARD_LR = {16, 18, 25, 27, 29, 31}
# Wk 26 was a TT week; it is now a real race on the Sunday (see DAY_OVERRIDE).
TT_WEEKS = {10, 13}

# Weeks written off in advance — travel, festivals, anything where training genuinely isn't
# happening. Planned downtime beats a week of sessions marked missed: the ramp steps down
# into it and rebuilds out of it, instead of pretending the week existed and leaving the
# runner to "catch up", which is how a break turns into an injury.
OFF_WEEKS = {6: "Lost Village"}
# First week back. Volume returns before intensity does — reintroducing threshold work in
# the same week as the mileage is the classic way to convert a planned break into a strain.
EASY_RETURN_WEEKS = {7}
# qkm() sizes the quality sessions per phase, which assumes the phase's usual volume. In the
# rebuild weeks the week is far smaller than the base phase assumes, so the two quality runs
# would eat it whole and leave the easy days rounding to two or three km each.
QKM_OVERRIDE = {7: {"tue": 9, "thu": 9}, 8: {"tue": 10, "thu": 10},
                9: {"tue": 9, "thu": 10}, 10: {"tue": 11, "thu": 10},
                11: {"tue": 7, "thu": 9}, 13: {"tue": 12, "thu": 11},
                # Alternating K's is 12 km of continuous work; 15 km leaves no warm-up.
                25: {"tue": 18, "thu": 17}, 29: {"tue": 18, "thu": 17}}
# Days whose sessions trade places in a given week, applied after the week is built so the
# sizing logic above still sees its normal Tue/Thu quality slots. Wk 8: Sunday's long run
# was run on Monday, so Tuesday's tempo would have landed on tired legs — the session moves
# to Wednesday and Wednesday's easy run comes forward. The S&C tag travels with the session
# it's attached to, which is correct: the hard-day block belongs with the quality run.
DAY_SWAPS = {8: (("Tue", "Wed"),), 9: (("Tue", "Wed"), ("Thu", "Fri")), 11: (("Tue", "Thu"),),
             # Wk 15 asked for on Mon 26 Oct: Tue/Wed swapped for Cav and Jamie both,
             # so they run the quality session together on the Wednesday.
             15: (("Tue", "Wed"),)}
# Individual days rewritten wholesale, applied after the week is otherwise built. Wk 10:
# Ibiza 24-26 Sep, so the 5K test moves to Wednesday the 23rd — the last clear day. The
# days that remain carry as much volume as they can without wrecking the test: Monday takes
# the bulk (furthest from it), Tuesday stays short (a quality session the day before a time
# trial costs more than it gives), the test day is just 1 km either side of the 5K, and the
# Sunday travel day picks up an easy evening run instead of being written off.
DAY_OVERRIDE = {26: {"Wed": ("Easy 20 km + 6×20s strides  (double: split AM/PM)", "easy", 20),
                     "Thu": ("Medium-long 26 km easy — the week's long run, moved off the "
                             "weekend so Sunday's race is run on fresh legs", "long", 26),
                     "Fri": ("Recovery 12 km easy  +S&C (easy-day session)", "recovery", 12),
                     "Sat": ("Easy 8 km + 4×100 m strides — race primer, nothing more", "easy", 8),
                     "Sun": ("10K RACE — Salida del Sol, Málaga (flat seafront, ~8,000 runners, "
                             "~45 min away) · w/u 2 km · c/d 2 km. A real field is worth 20–40s "
                             "over a solo TT, which is why this replaces the time trial. "
                             "DATE UNCONFIRMED — the 2026 edition ran Sun 18 Jan; check the "
                             "organiser in November and tell me if it lands elsewhere", "race", 14)},
                21: {"Tue": ("Pre-race sharpener: 4×1 km @ 3:50/km, 90s jog @ 6:00/km · w/u 3.5 km "
                            "· c/d 2.5 km  +light S&C — half the usual threshold volume, "
                            "five days out", "quality", 11),
                     "Wed": ("Easy 10 km + 6×20s strides", "easy", 10),
                     "Thu": ("Easy 11 km — no medium-long this week, Sunday is the session", "easy", 11),
                     "Fri": ("Recovery 6 km easy  +light S&C (race week)", "recovery", 6),
                     "Sat": ("Shakeout: easy 6 km + 4×100 m strides at race pace", "easy", 6)},
                30: {"Tue": ("Easy 15 km + 6×20s strides — Thursday's test is the week's "
                            "priority; arriving at it with 9 km of threshold in the legs "
                            "would measure your Tuesday, not your fitness", "easy", 15)},
                33: {"Tue": ("Easy 10 km + 4×100 m strides", "easy", 10),
                     "Wed": ("Easy 8 km — last real run, stay relaxed", "easy", 8),
                     "Thu": ("Easy 6 km + 4×100 m strides", "easy", 6)},
                12: {"Tue": ("Rest — couldn't run today", "rest", 0),
                     "Wed": ("Easy 18 km — Tuesday's session shifted; keep it genuinely easy, "
                             "HR under 153, so Thursday's tempo isn't compromised", "easy", 18),
                     "Thu": ("Tempo: 6 km continuous @ 3:58/km + w/u & c/d  "
                             "+S&C (hard-day session)", "quality", 13)},
                11: {"Thu": ("Recovery 6 km easy — feeling rough, so the 5K test moves to "
                             "the weekend  +S&C (easy-day session)", "recovery", 6),
                     "Fri": ("Rest — the 5K test moved on again, to Saturday morning", "rest", 0),
                     # Run 3 Oct: 2.07 km w/u, 5.02 km in 18:22 (watch 5K split 18:15), 0.69
                     # km c/d. Point-to-point and net downhill: altitude 279.2 m -> 218.6 m,
                     # so -60.6 m over 5.03 km = -1.21% average grade. Strava's GAP for the
                     # effort is 3:41/km = 18:25 for 5 km, i.e. the descent was worth only
                     # ~1 s/km. (I first applied Minetti's metabolic-cost curve directly to
                     # pace and got 19:10-19:30 — wrong: braking forces mean you cannot
                     # convert the full metabolic saving of a downhill into speed. Strava's
                     # GAP is empirically fitted and is the right tool here.) VDOT ~54.8.
                     "Sat": ("5K TIME TRIAL — 18:22 for 5.02 km (GAP 3:41/km = 18:25 flat). "
                             "A PR by ~57s. HR 176 avg / 183 max", "tt", 8)},
                9: {"Thu": ("Recovery 9 km easy (half of Saturday's run moved here)  "
                            "+S&C (easy-day session)", "recovery", 9),
                    "Fri": ("Hill strides: easy 13 km + 8×15s hill sprints "
                            "(half of Saturday's run moved here)", "easy", 13),
                    "Sat": ("Rest — Saturday's 6 km split across Thursday and Friday",
                            "rest", 0)},
                8: {"Thu": ("Rest — Thursday's run moved to Friday (no time)", "rest", 0),
                    "Fri": ("Easy 15 km + 6×20s strides (Thu + Fri combined)  "
                            "+S&C (easy-day session)", "easy", 15)},
                10: {"Mon": ("Easy 8 km + 6×20s strides (TT primer)", "easy", 8),
                     "Tue": ("Easy 7 km — genuinely easy, Z1 (130–140 bpm). Moving house + bad "
                             "sleep, so the 5K test moves to Tue 29th rather than being wasted", "easy", 7),
                     "Wed": ("Long slow 22 km — new longest run ever. Cap HR at 155 and let "
                             "pace be whatever that needs (evening ~5:05–5:15, daytime heat "
                             "5:30+). Conversational throughout or you're doing it wrong. "
                             "Fuel it: 750 ml with 45 g sugar + ¼ tsp salt, sipped from 40 min. "
                             "If the house move has left you wrecked, 16–18 km still counts", "long", 22),
                     "Thu": ("Rest — no time before the flight; the 8 km moves to Sunday", "rest", 0),
                     "Sun": ("Easy 18 km — evening, back from Ibiza (10 km + Thursday's 8). "
                             "Genuinely easy, HR under 150. Three days off running means the legs "
                             "will be fine; sleep and alcohol are the limiter. Bail to 12 km without "
                             "hesitation if Ibiza took more than expected — Thursday's 5K test is "
                             "worth far more than these 6 km", "easy", 18)}}
# Weeks cut to only the listed days; every other day becomes rest. Distinct from OFF_WEEKS,
# which writes off a whole week — here the surviving sessions are the point of the week.
KEEP_ONLY = {10: ("Mon", "Tue", "Wed", "Thu", "Sun")}
KEEP_ONLY_WHY = {10: "Ibiza"}
# Long runs set by hand for a given week, overriding the LR array. The week's volume moves
# by the same delta so the midweek days keep their own distances instead of being squeezed
# to pay for a longer Sunday. Wk 8: half-marathon long run, run on request — note this is
# a 51% jump on the 14 km actually run the week before, and longer than every long run
# scheduled up to Wk 12.
LR_OVERRIDE = {8: 21.1}
# Weekly volume set by hand, overriding VOL. Wk 11 is the week back from Ibiza: the array
# had 66 km, which is a doubling on the 31 km week before it and triple the ~22 km/wk
# actually being run through late Aug/early Sep. Trimmed to 52 with the 20 km long run
# kept intact — the long run is the part worth protecting, so the midweek days absorb
# the cut.
# Wk 21 was 80 km with a 7.5 km threshold session on the Tuesday and a 16 km
# medium-long on the Thursday, five and three days before Sevilla. Sevilla is the
# first hard effort of the whole block run in cool air, so it is the most
# informative day in the plan — worth more than the session it costs to protect it.
# Cut to 68, all of it from the five days before the race; the race itself and the
# Sunday distance are untouched. See DAY_OVERRIDE[21].
VOL_OVERRIDE = {9: 57, 11: 57, 12: 63, 13: 69, 21: 68, 26: 95}

# Trip bookings that have a real deadline, pinned to the day you have to act. The
# itinerary itself lives in plan/trip.py; these are only the things that are gone if you
# miss the date. Rendered under the day's session, never above it — the run is still the
# point of the page.
REMINDERS = {
    # Flights are a price-watch, not a calendar date. The published windows for Asia
    # long-haul are 3-5 months (Points Guy / Travel Market News, both off Google Flights
    # data) and 60-180 days (Going), and Google's own route analysis found US-Europe fares
    # bottoming near 129 days out. Departure is 27 Feb 2027, so the window is open NOW and
    # closing, not opening in November. Track, then book on a dip, with a hard backstop.
    "2026-10-19": ["✈️ Set Google Flights price alerts TODAY — this is an open-jaw: "
                   "Málaga → Tokyo (27 Feb) and Naha → Málaga (29 Mar), booked as one "
                   "multi-city ticket, not two returns. Price the alliance routings (one-world via "
                   "LHR/HEL, SkyTeam via AMS/CDG) separately — on an open-jaw, which fare buckets "
                   "are open matters more than the day you buy.",
                   "🏨 Book the Tokyo race-weekend hotel today too. Free-cancellation rates "
                   "mean there is no downside to booking early, and marathon-weekend rooms near the "
                   "start (Shinjuku) and finish (Tokyo Station) only move one way."],
    "2026-12-28": ["✈️ FLIGHT BACKSTOP — 60 days out. If the alert has not given you a dip "
                   "worth waiting for, book today anyway. Past this point fares climb, and Tokyo "
                   "Marathon weekend plus the start of sakura season on the return leg is the worst "
                   "possible pair of dates to be holding out on."],
    "2027-01-04": ["🎫 teamLab tickets (Borderless, Azabudai Hills) for Mon 1 Mar — timed entry, "
                   "weekends sell out. Book now that you are inside the release window.",
                   "🚆 Sagano Romantic Train (11 Mar) — reserved seats, sells out in sakura season.",
                   "🥃 Yamazaki Distillery tour (13 Mar) — lottery/release opens months ahead.",
                   "🥋 Check the sumo on-sale dates while you are at it — masu boxes "
                   "sometimes open on an earlier date than chair seats, and one source has general "
                   "sales starting ~2 months out, i.e. mid-January. If the dates have moved, tell me "
                   "and I will shift the 6 Feb reminder.",
                   "🪪 Apply for the International Driving Permit — required for the Mario Kart "
                   "go-karting on 1 Mar, and it is posted to you, so it is not a last-week job."],
    "2027-02-08": ["⏰ GHIBLI IN 48 HOURS. Set a real alarm for 01:55 Wednesday morning and make sure "
                   "your Lawson Ticket account already exists and is logged in — registering on the "
                   "day is how people miss it."],
    "2027-02-10": ["🎫‼️ GHIBLI MUSEUM TICKETS ON SALE — 02:00 CET TONIGHT (10:00 JST). "
                   "March entry is released today and the popular slots go in minutes. You want Fri 5 Mar. "
                   "Note this is the night before your 4×3 km readiness test — buy the tickets, then "
                   "go straight back to bed; you have all of Wednesday to recover."],
    "2027-02-06": ["🥋 Haru Basho (Osaka) tickets — advance sales open TODAY, 6 Feb. The 2027 "
                   "basho runs 14–28 Mar at EDION Arena Osaka, so the Osaka leg has to sit on or "
                   "after 14 Mar for this to exist at all. Buy the morning it opens — Haru Basho "
                   "sells out.",
                   "🎫 BUY: chair seats (isu-seki), 2×, via sumo.pia.jp/en — the English "
                   "route. They sell individually, have backrests and a raised view. Do NOT book "
                   "masu-seki: those tatami boxes sell as a whole box of four, so two of you pay "
                   "for four, and you sit on cushions with no back for five hours. Osaka 2026 "
                   "reference prices were ~¥3,500–11,000 per chair seat and ~¥34,000–60,000 per "
                   "4-person box — guides disagree, so treat these as a ballpark and read the "
                   "actual 2027 listing. Your day is a WEEKDAY, which is the cheap easy end; "
                   "weekends and the closing days go first.",
                   "⏰ Top-division (makuuchi) bouts run roughly 15:45–18:00 and the build-up is "
                   "slow, so arriving ~15:00 is plenty — no need to burn the whole day on it."],
    "2027-02-22": ["📱 Visit Japan Web — register immigration + customs now and save the QR codes "
                   "offline. Check in for the flight, and put every booking confirmation in one folder."],
    "2027-03-04": ["🎽️ EXPO — collect your race bib. Attendance is mandatory, there is no "
                   "race-day collection, and the expo closes before Saturday evening. Do it today, not "
                   "Saturday: standing in a queue for three hours two days out is a cost you do not need."],
}

def lr_for(w):   return LR_OVERRIDE.get(w, LR[w-1])
def vol_for(w):  return VOL_OVERRIDE.get(w, VOL[w-1]) + (lr_for(w) - LR[w-1])

# First week whose quality paces come from the 3 Oct 5K rather than the 19:22 PR.
RECALIBRATED_FROM = 12

def phase(w):
    if w <= 4:  return "Re-entry / Rebuild"
    if w <= 13: return "Aerobic Base"
    if w <= 23: return "Marathon-Specific I"
    if w <= 30: return "Specific II / Peak"
    return "Taper & Race"

def tue(w):
    if w <= 4:   return "Easy 10 km + 6×20s strides", "easy"
    if w <= 13:
        # Wk 5-11 quality was written off the 19:22 PR. The 3 Oct test was net downhill
        # (see DAY_OVERRIDE wk 11), so it confirms roughly PB-level fitness rather than a
        # minute of improvement — VDOT ~52, not the 55.5 a flat 18:15 would imply. Paces
        # move only as far as that supports. Weeks 5-11 keep the old numbers: they are the
        # record of what was actually prescribed, and regenerating them would make the log
        # claim sessions that were never set.
        # Threshold moved 3:55 -> 3:50 on 12 Oct 2026, against Daniels rather than with it.
        # VDOT 54.8 puts T at 3:57/km, so 3:55 was already textbook. The HR says the book
        # is wrong for him: the 8 Oct tempo held 3:59/km with HR plateauing 168-169, which
        # is 81% HRR against a threshold HR of 172-176 — comfortably sub-threshold, and HR
        # was flat not drifting. Interpolating his own two anchors (3:41/km -> HR 176 on
        # the 3 Oct 5K; 3:59/km -> 168 on 8 Oct) gives ~2.2 s/km per bpm, so reaching 173
        # means ~3:48. 3:50 for broken reps, 3:55 continuous. He has a marathon background
        # and a high threshold fraction of VO2max, which is exactly the shape that makes
        # VDOT-from-5K under-read T pace. The 17 Oct 10K TT settles it either way.
        # JOG RECOVERY 6:00/km everywhere. Two reasons it is written on every session
        # rather than left to feel. (1) It is exactly what the volume model assumes
        # (content.py note_wu jog_s=360), so the stated recovery and the w/u + c/d
        # distances can never disagree. (2) On 20 Oct 2026 his 2:30 recovery jogs
        # actually ran 6:30 / 7:07 / 8:35 / 13:11 - the last one is standing around.
        # A decaying recovery is both a fatigue signal worth seeing and a change to
        # the session itself: it is part of why that VO2 set under-stimulated VO2max.
        # Distinct from the FLOAT paces (4:15 alternating K's, 4:28 MP tempos), which
        # are not recoveries - see the comment in thu().
        lib = (["Threshold: 5×1 km @ 3:50/km (T), 90s jog @ 6:00/km", "Tempo: 2×3 km @ 3:55/km, 3 min jog @ 6:00/km",
                "Threshold: 6×1 km @ 3:50/km, 75s jog @ 6:00/km", "Tempo: 6 km continuous @ 3:55/km"]
               if w >= RECALIBRATED_FROM else
               ["Threshold: 5×1 km @ 4:10/km (T), 90s jog @ 6:00/km", "Tempo: 2×3 km @ 4:15/km, 3 min jog @ 6:00/km",
                "Threshold: 6×1 km @ 4:08/km, 75s jog @ 6:00/km", "Tempo: 6 km continuous @ 4:15/km"])
        return lib[(w-5)%len(lib)], "quality"
    if w <= 23:
        lib=["VO2: 5×1000 m @ 3:28/km (I), 2:30 jog @ 6:00/km","Threshold: 4×2 km @ 3:50/km, 90s jog @ 6:00/km",
             "VO2: 6×1000 m @ 3:26/km, 2:30 jog @ 6:00/km","Threshold: 5×1.5 km @ 3:48/km, 75s jog @ 6:00/km"]
        return lib[(w-14)%len(lib)], "quality"
    if w in (25, 29):
        # Alternating K's (the Italian "alternazioni"). The float is the recovery, so all
        # 12 km are run: 3:50 is LT2, 4:15 is LT1, and the whole thing averages ~4:03 —
        # essentially MP. That is the mechanism: it loads both ends of the aerobic range
        # in one continuous effort, which is what narrows the LT1–LT2 gap. Replaces the
        # rotation's 5×1.6 km in both weeks so the two are directly comparable.
        return ("Alternating K's: 6×(1 km @ 3:50/km / 1 km float @ 4:15/km) — 12 km "
                "continuous, no standing rest, averages ~4:03/km · w/u 3.5 km · c/d 2.5 km"), "quality"
    if w <= 30:
        lib=["Threshold: 6×1.5 km @ 3:48/km, 60s jog @ 6:00/km","Race reps: 5×1.6 km @ 3:52/km, 90s jog @ 6:00/km",
             "Threshold: 3×3 km @ 3:50/km, 2 min jog @ 6:00/km","VO2/sharpen: 6×800 m @ 3:24/km, 2 min jog @ 6:00/km"]
        return lib[(w-24)%len(lib)], "quality"
    return {31:"Threshold: 4×1 km @ 3:50/km, 90s jog @ 6:00/km",32:"Sharpen: 3×1 km @ 3:48/km, 2 min jog @ 6:00/km",
            33:"Easy 8 km + 4×100 m strides"}[w], ("quality" if w<33 else "easy")

def thu(w):
    if w <= 4:   return "Easy 8 km", "easy"
    if w <= 13:
        # distance comes from qkm so the text can't drift from target_km when a rebuild
        # week overrides it (see QKM_OVERRIDE)
        k = qkm(w, "thu")
        if w in EASY_RETURN_WEEKS:  # no hill sprints in the first week back
            return f"Easy {k} km + 6×20s strides", "easy"
        return (f"Hill strides: easy {k} km + 8×15s hill sprints" if w % 2
                else f"Medium easy {k} km + 6×20s strides"), "easy"
    if w == 22:
        # Four days after an all-out half — the rotation would otherwise land 10 km of
        # MP here. Sunday is already easy for the same reason.
        return f"Medium-long {qkm(w,'thu')} km easy — 4 days post-Sevilla", "easy"
    if w <= 23:
        # FLOAT PACE 4:28/km on the MP tempos. The float is recovery that never stops
        # working: the point of these sessions is one continuous aerobic stimulus, so the
        # float has to be slow enough to shed a few beats and fast enough that the legs
        # never unload. 4:28 is ~30 s/km off MP (3:59) and sits between MP and easy
        # (4:50-5:05); a 6:00 jog would dump 20+ beats and split the session into two
        # separate tempos. At 4:28 the whole continuous block averages ~4:01/km, i.e. MP
        # start to finish. Do NOT reuse the alternating-K's 4:15 here - that float is
        # relief from THRESHOLD (3:50), so it is scaled to a faster work pace.
        # Session check: if HR falls more than ~8 beats across the float, it was too slow.
        lib=["MP tempo: 2×5 km @ 3:59/km (MP), 3 min float @ 4:28/km","Medium-long 16 km w/ middle 8 km @ MP",
             "MP tempo: 3×4 km @ MP, 2 min float @ 4:28/km","Medium-long 16 km easy + 8×15s hill sprints"]
        return lib[(w-14)%len(lib)], "quality"
    if w == 30:
        # Readiness test, 4 weeks out. Replaces the rotation's 2×8 km @ MP in the same
        # MP slot and on the same 22 km day, so nothing is reshuffled and it adds no
        # third hard day. At 3:50 this is no longer an MP rehearsal — it is an LT2
        # test, 12 km at threshold off 90s jog. That is the right question anyway: a
        # 2:48 needs MP to sit only ~9 s/km off threshold, which is an elite-durability
        # gap, and the gap is exactly his weak point. It is also the first validation of
        # the 3:50 T pace itself, which was set from wrist-HR reasoning in Oct 2026.
        return ("READINESS TEST: 4×3 km @ 3:50/km (LT2), 90s jog @ 6:00/km — "
                "PASS = all four on pace, rep 4 no slower than rep 1, HR flat at 172–176 "
                "across reps 2–4. Fading to 3:55+ by rep 3 means 3:59 MP is optimistic. "
                "↑ IF THE BLOCK HAS GONE WELL: 3:45/km is the stretch version — but that is "
                "~10K race pace, so 12 km of it asks for 45 min at a pace you can only hold for "
                "37:40. Only take it if the wk-25 and wk-29 alternating K's both felt controlled "
                "AND Sevilla came in under 1:22:30. Decide at the warm-up, not in advance, and "
                "bail to 3:50 after rep 1 if it is not there — a failed test tells you nothing"), "quality"
    if w <= 30:
        lib=["MP: 3×6 km @ 3:59/km, 3 min jog @ 6:00/km","Medium-long 18 km w/ 10 km @ MP",
             "MP: 2×8 km @ MP, 3 min float @ 4:28/km","Medium-long 17 km easy"]
        return lib[(w-24)%len(lib)], "quality"
    return {31:"Easy 8 km + 4×20s strides",32:"Easy 8 km + 6×20s strides",33:"Rest or easy 5 km"}[w], "easy"

def sun(w):
    # via lr_for so the text can't drift from target_km when a week overrides its long run
    d=lr_for(w)
    txt={16:"28 km, last 8 km @ MP",18:"32 km, last 10 km @ MP",
        19:"30 km easy (recovery weekend — no MP)",
        20:"28 km easy — steady week, race is next Sunday",
        21:"TUNE-UP: Sevilla Half Marathon (all-out) · w/u 2 km · c/d 1 km",
        22:"30 km easy (post-race — keep it genuinely easy)",
        23:"20 km easy — Christmas week, keep it light",
        24:"24 km easy — New Year week, ease back in",
        25:"32 km, last 10 km @ MP — ramp resumes",
        26:"28 km easy (recovery weekend — no MP)",
        27:"38 km easy — longest run of the block, pure time on feet, no MP",
        28:"32 km easy (recovery weekend — no MP)",
        29:"35 km, last 12 km @ MP (dress rehearsal)",
        30:"32 km easy — FINAL long run, keep it relaxed",
        31:"21 km, last 8 km @ MP",32:"18 km easy w/ 4×1 km @ MP",
        33:"RACE DAY — Tokyo Marathon · 2:48 target · 3:59/km · 6:24/mi · halfway 1:24:00"}
    t = txt.get(w, f"{d:g} km easy" + (" + last 4 km relaxed @ MP" if w == 12 else ""))
    return t, ("race" if w in (21,33) else "long")

def sat(w):
    if w == 10: return "parkrun 5K — TIME TRIAL (fitness check) + w/u & c/d", "tt", 9
    if w == 13: return "10K TIME TRIAL or local race (fitness check) + w/u", "tt", 13
    if w == 33: return "Shakeout: easy 4 km + 4×100 m strides", "easy", 4
    return None, "easy", None

def qkm(w, which):
    if w in QKM_OVERRIDE: return QKM_OVERRIDE[w][which]
    if w <= 4:  return {"tue":10,"thu":8}[which]
    if w <= 13: return {"tue":13,"thu":11}[which]
    if w <= 23: return {"tue":14,"thu":16}[which]
    if w <= 30: return {"tue":15,"thu":{24:24,28:24,30:22}.get(w,17)}[which]
    return {"tue":9,"thu":8}[which]

def build_week(w):
    v=vol_for(w); lr=lr_for(w); reentry = w<=4
    if w in OFF_WEEKS:
        # Written off deliberately, so it reads as a plan rather than as seven missed
        # sessions. Nothing is carried over into the week either side — a week's training
        # can't be banked, and trying to make it up is what causes the damage.
        why = OFF_WEEKS[w]
        days = {d: (f"Off — {why}", "rest", 0) for d in DOW}
        days["Sun"] = (f"Off — {why}. Easy running resumes Monday; don't make this week up.",
                       "rest", 0)
        return days
    tue_txt,tue_type = tue(w); thu_txt,thu_type = thu(w); sun_txt,sun_type = sun(w)
    tue_km=qkm(w,"tue"); thu_km=qkm(w,"thu")
    # Volume comes back before intensity does — see EASY_RETURN_WEEKS.
    easy_return = w in EASY_RETURN_WEEKS and tue_type == "quality"
    if easy_return:
        tue_txt, tue_type = f"Easy {tue_km} km + 6×20s strides (first week back — no quality yet)", "easy"
    tue_txt = C.note_wu(tue_txt, tue_type, tue_km)
    thu_txt = C.note_wu(thu_txt, thu_type, thu_km)
    sat_txt,sat_type,sat_fixed = sat(w)
    days={}
    # BJJ — SCHEDULED, NOT SQUEEZED INTO THE GAPS (added 22 Oct 2026, his decision).
    # Friday is the only day of the week with nothing hard behind it: Mon sits in front
    # of Tue quality, Wed in front of Thu quality, Sat in front of the long run. In wk 14
    # the two sessions landed on Mon and Wed — the two worst squares — and both quality
    # days showed it (Tue capped at 176 with maximal RPE at 85% HRR; Thu drifted +7 bpm
    # between reps at an identical 3:59/km). So: Fri is the main session, Mon is drills.
    # NO LIVE SPARRING FROM WK 15, his own rule — he stops once the weeks reach 80-90 km,
    # and wk 15 is the first at 84. It is ONE-WAY: wks 17/21/23 dip back to 76/68/76 but
    # sparring does not resume, because coming back to live rounds deconditioned, against
    # partners who never stopped, is when people get hurt — and wk 21 is Sevilla week.
    # Drilling is roughly a third of the systemic cost of sparring, not zero, so it still
    # gets a slot and still never precedes a quality day. The Friday S&C moves to Monday
    # to pair with it: both low-intensity, and Fri was otherwise carrying a run, S&C and
    # two hours of mat time. Expect this to fall back to Friday-only in the peak block —
    # at 107-116 km with 32-38 km Sundays the week runs out of days.
    mon_txt = "Rest" if (reentry or w==33) else "Rest / mobility (full rest day)"
    if 15<=w<=30 and not reentry:
        mon_txt = "Rest from running · BJJ drills/technical, no live rounds  +S&C (easy-day session)"
    days["Mon"]=(mon_txt,"rest",0)
    if 4<=w<=30:
        tue_txt += "  +S&C (easy-day session)" if easy_return else "  +S&C (hard-day session)"
    # Max 2 hard days/week: Thu is quality only when Sunday's long run is easy and there's no Sat TT
    hard_sun = sun_type == "race" or w in HARD_LR
    if thu_type == "quality" and (hard_sun or w in TT_WEEKS):
        thu_txt, thu_type = f"Medium-long {thu_km} km easy", "easy"
    known=lr+tue_km+thu_km+((sat_fixed or 0) if w in TT_WEEKS else 0)
    if w==33: known=0
    pool=max(v-known,0)
    if reentry:
        wed_km=round(pool*0.55); fri_km=max(pool-wed_km,0); sat_km=0
    elif w in TT_WEEKS and sat_fixed:
        # Saturday's distance is set by the test, so the residual that would normally
        # land there has nowhere to go and silently vanished — the week's days stopped
        # summing to its own target_km. Split the pool between Wed and Fri instead.
        fri_km=round(pool*0.40); wed_km=max(pool-fri_km,0); sat_km=0
    else:
        fri_km=round(pool*0.28); wed_km=round(pool*0.40); sat_km=max(pool-fri_km-wed_km,0)
    wed_txt=f"Easy {wed_km} km"+("" if reentry else " + 6×20s strides")
    if reentry:
        fri_txt,fri_type,fri_kmv=f"Easy {fri_km} km","easy",fri_km
    elif w==33:
        fri_txt,fri_type,fri_kmv="Rest","rest",0
    else:
        if 15<=w<=30:
            # S&C moved to Mon; this is the week's main mat session, drills only
            fri_txt=f"Recovery {fri_km} km easy  +BJJ (drills only — no live rounds)"
        else:
            fri_txt=f"Recovery {fri_km} km easy"+("  +light S&C (taper)" if 31<=w<=32 else "  +S&C (easy-day session)")
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
    for a,b in DAY_SWAPS.get(w,()):
        days[a],days[b]=days[b],days[a]
    for dow,spec in DAY_OVERRIDE.get(w,{}).items():
        days[dow]=spec
    keep=KEEP_ONLY.get(w)
    if keep:
        why=KEEP_ONLY_WHY.get(w)
        for dow in DOW:
            # days already resting keep their own wording; only real sessions are cleared
            if dow not in keep and days[dow][1]!="rest":
                days[dow]=(f"Rest — {why}" if why else "Rest","rest",0)
    return days

def focus(w):
    return {6:"🎪 Lost Village — planned week off",7:"Back from the break — rebuild, no quality",
            10:"5K time trial Wed, then Ibiza 24-26 Sep",13:"10K time-trial checkpoint",
            21:"Half tune-up (calibrate goal)",23:"🎄 Christmas week — deliberate holiday dip",
            24:"🎆 New Year week — easing back in",25:"Ramp resumes (from the day after NYD)",
            28:"Peak volume week",
            30:"✅ 4×3 km readiness test — last call to confirm or move the goal",
            29:"Peak long run",33:"RACE WEEK"}.get(w, "Cut-back / recovery week" if w in (4,17) else "")

DOW=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

def content():
    return {
        "shoes": {
            "intro": "Five pairs to the start line, 1,910 km to cover. Rotating rather than "
                     "wearing one pair out is the point — varying the loading pattern is "
                     "associated with materially lower injury risk, and that matters more at "
                     "90-116 km/wk than which model you pick. Every session on the plan is "
                     "tagged with its shoe.",
            "headers": ["Shoe", "Used for", "km from Wk 12", "Total at Tokyo", "When to buy"],
            "rows": [
                ["Daily trainer", "Easy + recovery", "472", "472", "Now — firmer, neutral (Ride / Pegasus / Kiprun KD500)"],
                ["Max-cushion (long-run)", "Every long run", "449", "449", "Now — soft and high-stack (Nimbus / Skyflow / Kiprun KS900)"],
                ["Daily trainer #2", "Easy + recovery from Wk 20", "374", "374", "Early Jan, as the first nears 500 km"],
                ["Mach X3", "Most quality sessions", "296", "462", "Owned — 166 km"],
                ["EVO SL", "Quality, every third week", "166", "545", "Owned — 379 km. Retire after Tokyo."],
                ["RACE SHOE", "Sevilla, Tokyo + 2 bed-in runs", "128", "128", "Early-mid Nov — Metaspeed Sky / Alphafly 3 / Adios Pro 5"],
            ],
            "note": "The racer holds its bounce for ~250-300 km, so it only appears four times: "
                    "one MP long run to bed it in before each race (Wk 18, and the Wk 29 dress rehearsal), Sevilla on 13 Dec, and Tokyo. "
                    "Don't train in it. Buy it in November rather than January so a bad fit turns up "
                    "at the half and not three weeks out — super shoes change calf and Achilles "
                    "loading noticeably and not everyone gets on with a given geometry. "
                    "Log mileage per pair in Strava (assign gear to each activity); most "
                    "worn-shoe injuries happen because nobody was counting.",
        },
        "paces": {"headers": ["Zone", "per km", "per mile", "Use"], "rows": [
            ["Recovery", "5:35–6:05", "8:59–9:47", "Easy shakeouts, doubles, day-after"],
            ["Easy / aerobic", "5:00–5:35", "8:03–8:59", "Bulk of weekly volume (incl. doubles)"],
            ["Long-run easy", "4:55–5:30", "7:55–8:51", "Long-run base portions"],
            ["Marathon (MP)", "3:59", "6:24", "Race pace — MP blocks & long-run finishes"],
            ["Threshold (T)", "3:50–3:55", "6:10–6:18", "Tempo / cruise intervals — HR 172–176, not pace-led"],
            ["10K pace", "3:46", "6:04", "Longer VO2 / race sharpeners"],
            ["Interval (I, 5K)", "3:35–3:40", "5:46–5:54", "VO2 max reps"],
            ["Strides", "~3:10 feel", "relaxed-fast", "20s pickups, not a workout"]],
            "note": "T/10K/I paces come from the 3 Oct time trial — 18:22 actual, Strava GAP 3:41/km = 18:25 flat-equivalent, VDOT ~54.8 — NOT from the 2:48 goal. Training paces have to match the engine you have, and goal-anchored threshold work is just racing in disguise. Moving the goal 2:50 → 2:48 therefore moved ONE row: MP, 4:01 → 3:59. Threshold, 10K and interval paces are unchanged, because your physiology did not change when the target did. HR TARGETS BELOW ARE PROVISIONAL — every HR figure anchoring them came from a wrist optical sensor, which under-reads and cadence-locks on exactly the hard efforts that matter. Re-establish them with the chest strap before trusting any bpm number. Recalibrate pace at the Wk-21 half. Run easy days and ALL doubles genuinely easy — conversational. Max 2 hard days per week: "
                    "Tue quality plus EITHER the Thu session OR a Sunday MP long run — never both. Hard "
                    "long-run weekends always alternate with easy ones."},
        "checkpoints": {
            "intro": "2:48 is the A-goal, and it is a number with a reason: Boston's 18-34 standard is 2:55, but the 2027 cut-off came in 5:17 UNDER that, so 2:49:43 was the real entry time. 2:48 buys ~2 min of margin against a cut-off that moves every year (6:51 in 2025, 5:29 in 2024). 2:50 would have missed by 17 seconds. The 3 Oct 5K read 18:22 on a net -60 m course; Strava GAP puts it at 3:41/km = 18:25 flat, so a genuine PR by ~57s and VDOT ~54.8 — which is a ~2:56 engine on the Daniels tables, not yet a 2:48 one. Two things have to move: the engine, and the mileage behind it — 13 weeks in, the average is ~43 km/wk against a 116 km peak, and under-trained runners finish well behind what a 5K says they are worth. The mileage IS the plan; the engine follows it. "
                     "Don't lock race-day pace until the Wk-21 half.",
            "headers": ["Wk / date", "Test", "On-track for 2:48", "If short — likely target"], "rows": [
                ["Wk 11 · Sat 3 Oct ✓", "5K TT — 18:22 (GAP 18:25, PR by ~57s)", "done", "VDOT ~54.8 · ~2:56 engine — mileage is the gap to 2:48"],
                ["Wk 13 · Sat 17 Oct — VOID", "10K TT — 39:22 raw · ~37:36-38:11 corrected", "≤ 37:20", "Not a measurement, but corrected it corroborates the 5K. Next honest test is Sevilla."],
                ["Wk 21 · Sun 13 Dec", "Half-marathon — Sevilla Half, signed up",
                 "≤ 1:22:00 · 3:53/km · 6:15/mi",
                 "1:22:00–1:22:30 live but tight · 1:22:30–1:23:30 needs everything to go right, decide at Wk 30 · >1:23:30 → re-target 2:52–2:55"],
                ["Wk 30 · Thu 11 Feb", "4×3 km @ 3:50/km (LT2), 90s jog @ 6:00/km — readiness test",
                 "All four on pace, rep 4 ≥ rep 1, HR flat 172–176",
                 "Fading to 3:55+ by rep 3 → LT2 isn't at 3:50, so run Tokyo at 2:52–2:55"],
                ["Race · 7 Mar", "Marathon", "2:48 = 3:59/km · halfway 1:24:00", "Start at CONFIRMED pace. Even splits."]],
            "notes": [
                "WK-13 10K IS VOID AS A TEST, BUT IT IS NOT A BAD SIGN (17 Oct, 39:22). Four confounders, all disclosed: ~7 pints the night before, diarrhoea during the warm-up, 23-24°C AND 80-90% humidity. The humidity is the one that matters most and was learned last: at 23.5°C/85% the dew point is 20.8°C and the wet bulb 21.6°C, so temp+dewpoint = 144°F, which sits in the 3.0-4.5% band. That is 71-106s over 10K, giving a corrected 37:36-38:11 against a 5K-predicted 38:18 (Riegel 1.06) — i.e. the corrected time MATCHES OR BEATS the prediction across the whole band, with the alcohol and GI handicaps still unaccounted for on top. So: too many uncontrolled variables to read a number off it, but it corroborates VDOT 54.8 rather than undercutting it. The HR (164 avg) was wrist-only and should be ignored outright. Do NOT re-run it — Sevilla on 13 Dec is the next honest test, and it will also be the first hard effort of the block run in cool conditions.",
                "SEVILLA PACING — the number is 1:22:00, and it is not just read off a Riegel table. 2:48 off an ORDINARY conversion needs about 1:20:45 of half fitness tapered and at peak; Sevilla is neither. Two things offset: wks 22-33 are the marathon-specific ones and a well-run twelve weeks there is worth ~1.5%, while racing untapered off a 68 km week costs ~1%. Net: 1:22:00 in December plus an ordinary twelve weeks arrives at 2:48 needing nothing exotic in March. Even-split pacing, per km / per mile / 5K / 10K / 15K / 20K: 1:21:30 = 3:52 / 6:13 / 19:19 / 38:38 / 57:57 / 1:17:16 · 1:22:00 = 3:53 / 6:15 / 19:26 / 38:52 / 58:18 / 1:17:44 · 1:22:30 = 3:55 / 6:18 / 19:33 / 39:06 / 58:39 / 1:18:12 · 1:23:30 = 3:57 / 6:22 / 19:47 / 39:35 / 59:22 / 1:19:09. DO NOT TRY TO PACE THE BANDS — 1:21:30 and 1:22:30 are 3 s/km apart, which is finer than anyone paces or than the chip timing resolves. Run 3:53 and let the clock sort it out. The one hard rule: do not go out at 3:50 and fade. A faded half is a contaminated data point — you will not know afterwards whether you were 1:22:30 fit or 1:21:00 fit and blew up, and the whole value of this race is that it is the first clean read of the block. Run 3:53 to 15 km, then spend whatever is left: Zaragoza was a negative split, so he can do this, and 1:21:30 off a strong last 6 km is worth more than 1:21:30 off a fade.",
                "BOSTON: hitting the standard does not get you in. The 2027 cut-off was 5:17 under, so 18-34 men needed 2:49:43 against a 2:55 standard, and ~8,000 qualifiers who beat the standard were still rejected. That is why the target is 2:48 and not 2:50. Two things soften it: the BAA now draws ~1,000 places at random from qualifiers who missed the cut-off, and your age group is set by your age on BOSTON race day (Apr 2028), not on race day in Tokyo — so turning 35 before then would drop the standard to 3:00 and change this whole target.",
                "Peak ~116 km — weekly volume is the biggest lever for marathon time, and the extra should be EASY km (your endurance lags your speed).",
                "Rest days are Monday (always) and Saturday in the re-entry weeks; race-week Friday rest is the one exception.",
                "Hard long runs alternate with easy ones — never two hard long-run weekends in a row, and the weekends before/after the Wk-21 half are easy.",
                "Wk 23 (Christmas) and Wk 24 (New Year) are a deliberate holiday dip — volume drops to ~76-88 km so the block doesn't fight the festive season. The ramp resumes from Wk 25, the week starting the day after New Year's Day.",
                "Injury risk is about ramp rate, not the ceiling — ~7–10% weekly steps; respect cut-back weeks (4,10,17) and the holiday dip (23,24).",
                "Wk 6 is Lost Village — a planned week off, not a missed week. Wk 7 comes back at 45 km with no quality session; volume returns before intensity does. Do NOT try to make up Wk 5 or Wk 6 — the rebuild already accounts for both.",
                "Re-planned Wk 20 Aug: the original ramp assumed ~56 km/wk by Wk 5, but weeks 1-5 actually averaged ~40. The new curve rebuilds from that, reaching the same 116 km peak at Wk 28 instead of Wk 27 — still 5 weeks out from the race.",
                "If 116 km proves unrealistic, the ~105 km version is still solidly sub-3."]},
        "strength": C.strength("1–13", "14–30", football=False),
        "warmup": C.warmup(niggle_note="Given the outside-left-ankle/Achilles soreness flagged in week 1, "
                                        "the banded eversion work and single-leg balance in this routine "
                                        "aren't optional extras for you right now — do them every session "
                                        "regardless of whether it's currently bothering you."),
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
        "layover": {
            "intro": "Long-haul connection through Beijing (PEK) on the way to Seoul, ~04:00-18:50 on the "
                     "ground. Long run gets done mid-layover instead of losing the day to travel — British "
                     "passport, so no advance visa needed for either stop: China's 30-day visa-free entry "
                     "(in effect through 31 Dec 2026) or the 240-hour transit rule covers Beijing, processed "
                     "at a dedicated counter on arrival; Korea's K-ETA is waived for UK passports through "
                     "31 Dec 2026, so nothing needed there either unless leaving the terminal, in which case "
                     "it's just the free digital e-Arrival Card.",
            "schedule": {"headers": ["Time", "What"], "rows": [
                ["04:00-04:45", "Land, visa-free entry counter"],
                ["04:45-05:00", "Customs, drop bag at T3 2F left-luggage — free for visa-free transit passengers"],
                ["05:00-05:35", "Airport Express + taxi to Olympic Green"],
                ["05:35-05:55", "Change, warm up"],
                ["05:55-07:40", "Long run — Olympic Forest Park loop(s), ~15-16 km"],
                ["07:40-08:00", "Cooldown/stretch"],
                ["08:00-08:45", "Shower/change (day-use hotel near the park, booked on Ctrip/Meituan same-day) + food"],
                ["08:45-09:00", "Subway to Line 8 (Olympic Sports Center station)"],
                ["09:00-10:00", "Shichahai/Houhai — lake, hutongs"],
                ["10:00-10:45", "Nanluoguxiang — hutong walk, food stalls"],
                ["10:45-11:30", "Jingshan Park — panoramic view over the Forbidden City roofs"],
                ["11:30-12:30", "Tiananmen Square / Qianmen — walk the square, lunch"],
                ["12:30-13:00", "Buffer / extra wandering"],
                ["13:00-13:45", "Subway/taxi back toward the airport"],
                ["13:45-14:30", "Arrive airport, retrieve bag"],
                ["14:30-15:15", "Check-in, security, exit immigration"],
                ["15:15-18:50", "Buffer / boarding"],
            ]},
            "notes": [
                "One line (Line 8) covers Olympic Green → Shichahai → Nanluoguxiang → Jingshan Park → Qianmen — "
                "no transfers, ~13 min Olympic Green to the hutongs.",
                "Skips the Forbidden City itself (needs a pre-booked ticket, easy to get caught out on short "
                "notice) — Jingshan Park gives the classic skyline shot without the queue/booking risk.",
                "Beijing in mid-August is hot and humid even early — lows ~22-24°C at 6am — hydrate well before "
                "the run, not just during.",
                "Day-use hotel rate near Olympic Green wasn't confirmed in advance research — estimated "
                "¥150-350 (~€20-45) by extrapolating from nightly rates; check live prices on Ctrip/Meituan "
                "on the ground.",
                "Assumes both legs route through PEK (Capital), not PKX (Daxing) — Daxing is much further from "
                "Olympic Green and would blow this schedule; double-check the boarding pass.",
            ],
        },
        "tips": [
            ["Volume is the big lever", "Marathon time tracks weekly mileage more than any other trainable factor — that's why the peak is ~116 km. Add it as EASY km."],
            ["Doubles > longer hard runs", "Two short easy runs add volume with less injury risk than lengthening workouts — that's how you reach ~116 km with a rest day intact."],
            ["Ramp is the risk, not the ceiling", "Injuries come from increasing load too fast for your base, not from high mileage itself. ~7–10% weekly steps."],
        ] + C.TIPS_COMMON,
    }


# ---------------------------------------------------------------- shoe rotation
# Five pairs covering 1,910 km to the race. Rotating rather than wearing one pair
# out is the point: varying the loading pattern is associated with materially lower
# injury risk, which matters more at 90-116 km/wk than any individual model does.
# Owned: Mach X3 (166 km at wk 12), Adizero EVO SL (379 km). Both firm and fast, so
# the two new trainers are the soft end of the rotation.
SHOES = {
    "daily":  "Daily trainer",
    "daily2": "Daily trainer #2",
    "long":   "Max-cushion (long-run)",
    "machx":  "Mach X3",
    "evosl":  "EVO SL",
    "race":   "RACE SHOE",
}
# The racer only comes out for the two races and the handful of MP sessions that
# bed it in — it holds its bounce for ~250-300 km and must not be spent on training.
# One bed-in run before each race. Wk 18 rather than 19 so there is a week in hand
# to react if the shoe does not suit. Wk 29 rather than 30 before Tokyo: 29 is the
# dress rehearsal (35 km with 12 km @ MP) and 30 is an easy run, so 29 is the one
# that actually rehearses race pace in race shoes.
RACE_SHOE_DAYS = {(18,"Sun"), (21,"Sun"), (29,"Sun"), (33,"Sun")}
# Second daily trainer arrives when the first is around 500 km.
DAILY2_FROM = 20

def shoe_for(w, dow, typ, sess):
    if typ == "rest":
        return None
    if (w, dow) in RACE_SHOE_DAYS:
        return SHOES["race"]
    if typ in ("race",):
        return SHOES["race"]
    if typ in ("quality", "tt"):
        # Weighted toward the Mach X3: it starts the block on 166 km against the
        # EVO SL's 379, and the EVO SL is a racer-trainer that should be retired
        # around 550 km rather than run into the ground through the peak weeks.
        return SHOES["evosl"] if w % 3 == 0 else SHOES["machx"]
    if typ == "long":
        return SHOES["long"]
    # easy + recovery share the two daily trainers; the second joins once the first
    # is near 500 km, and from then on they alternate so neither is worn out at peak.
    if w >= DAILY2_FROM and (w % 2 == 1 or typ == "recovery"):
        return SHOES["daily2"]
    return SHOES["daily"]


def build():
    weeks=[]
    for w in range(1,34):
        monday=START+timedelta(days=(w-1)*7); dm=build_week(w); days=[]
        for i,dow in enumerate(DOW):
            txt,typ,km=dm[dow]
            iso=(monday+timedelta(days=i)).isoformat()
            day={"date":iso,"dow":dow,"type":typ,"session":txt,"target_km":km,
                 "shoe":shoe_for(w,dow,typ,txt)}
            if iso in REMINDERS: day["reminders"]=REMINDERS[iso]
            days.append(day)
        weeks.append({"week":w,"start":monday.isoformat(),"phase":phase(w),
                      # a KEEP_ONLY week's volume is whatever survives, not the VOL array
                      "target_km":(round(sum(x["target_km"] for x in days),1) if w in KEEP_ONLY
                                   else vol_for(w)),"focus":focus(w),"days":days})
    return {"meta":{"id":ID,"name":NAME,"goal":GOAL,"mp_per_km":"3:59","mp_per_mile":"6:24",
                    "start":START.isoformat(),"race":RACE.isoformat(),
                    "peak_km":max(VOL),"total_weeks":33,
                    "goal_note":"Anchored on 2:48 (3:59/km) — the Boston 18-34 cut-off, not a round number. Calibrate at the Wk-21 half."},
            "weeks":weeks, "content":content()}
