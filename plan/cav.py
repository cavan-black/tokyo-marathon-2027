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
       # Wks 15-16 cut for the left subtalar/medial-ankle injury (onset 22 Oct,
       # forced a 1.6 km abort on 27 Oct). Was 84 and 90. Wks 17-20 are the
       # rebuild ramp back to it: 46/60/74/85, was 76/97/101/92. Each step is
       # 15-30% up, which is steep for new volume but reasonable for RE-attaining
       # volume he was already running in October. Wk 21 (Sevilla) and everything
       # from wk 22 are untouched, so the marathon-specific block is intact.
       76,29,36,46,60,74,85,80,96,76,
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
             # so they run the quality session together on the Wednesday. That left the
             # Wednesday threshold directly in front of the Thursday MP tempo, so Thu/Fri
             # swap too — threshold Wed, recovery Thu, MP Fri. Same weekly total, same two
             # quality sessions, but a day of easy running between them. Matters more than
             # usual this week: the missed wk 14 long run was run on Mon 26, so wk 15 lands
             # near 108 km on a four-week average of 64.
             15: (("Tue", "Wed"), ("Thu", "Fri"))}
# Individual days rewritten wholesale, applied after the week is otherwise built. Wk 10:
# Ibiza 24-26 Sep, so the 5K test moves to Wednesday the 23rd — the last clear day. The
# days that remain carry as much volume as they can without wrecking the test: Monday takes
# the bulk (furthest from it), Tuesday stays short (a quality session the day before a time
# trial costs more than it gives), the test day is just 1 km either side of the 5K, and the
# Sunday travel day picks up an easy evening run instead of being written off.
DAY_OVERRIDE = {
                # Wk 14's Sunday long run was not skipped — it was run the next morning,
                # Mon 26 Oct, and is logged there in wk 15. Leaving it as a due session here
                # counted one 24 km run as a miss in wk 14 and a tick in wk 15 at the same
                # time. It is a deferral, so the Sunday carries no target and the week's
                # volume drops to the 52 km that were actually due in it.
                14: {"Sun": ("Long run deferred — run on Mon 26 Oct instead, logged in wk 15",
                             "rest", 0)},
                # Cross-training key (HR from Karvonen 197/52, HRR 145, offset for mode —
                # bike runs ~5-10 bpm under running, deep water ~10-15 under):
                #   CT1 easy spin 45-60 min @ 133-148, cadence 90-95
                #   CT2 easy spin 45 min + 6x1 min high-cadence spin-ups @ 100-110 rpm
                #   CT3 bike threshold 4x6 min @ 163-172, 3 min easy between
                #   CT5 long bike 75-90 min @ 139-153
                # Two hard sessions a week is what holds VO2max; everything else genuinely
                # easy. No rowing or stair climber — both drive force through the footplate.
                # He opted out of aqua jogging (27 Oct), so this is bike-only. That costs a
                # little running-specific patterning, which the single-leg S&C work offsets.
                # ---- INJURY: left subtalar / medial ankle, onset 22 Oct 2026 ----
                # Felt on 22, 23, 24 and 26 Oct, then forced a 1.6 km abort on 27 Oct at
                # 5:33/km on the flat. Pain present from the first km of easy running is the
                # line where running stops being a judgement call. No bone tenderness and
                # strength tests were clean on 26 Oct, so this is soft tissue — but it has
                # worsened across five consecutive runs, so the fix is load removal, not
                # another shoe. Cross-training keeps the aerobic base; nothing weight-bearing
                # through a cornering or push-off load. No BJJ at all: mat work torques this
                # joint directly.
                # ---- REVISED 1 Nov: this is the THIRD event in the same left posterior
                # chain. March 2026 was left achilles pain at the musculotendinous junction,
                # bad enough to stop running. Around 2018 a football ankle/achilles sprain,
                # same side, on video. Two tendon episodes in one leg in eight months is a
                # capacity problem, not bad luck, and the likely root is deficits left over
                # from the sprain that were never rehabbed. That changes the treatment: rest
                # settles tendon symptoms while lowering tendon capacity, which is exactly
                # the March -> October loop. From here the ankle gets LOADED, daily, and
                # running returns early and small rather than late and big.
                # ---- REHAB, split by load. The split matters: tendon collagen synthesis
                # runs net-NEGATIVE for ~24-36 h after a heavy load and only turns positive
                # again around 48-72 h. Heavy work every day parks him in the catabolic half
                # of that cycle forever, which is the opposite of the goal. So:
                # DAILY (low load, ~8 min, both legs, run days included):
                #   R1 isometric calf hold 5x45 s single-leg mid-range, ~70% effort. Early
                #      analgesia and load tolerance without the recovery cost.
                #   R3 banded resisted inversion 3x15 slow — tib post direct
                #   R4 single-leg balance 3x30 s eyes closed — the 2018 sprain's legacy
                #   R5 short-foot / toe yoga 3x10 — intrinsics
                # GYM, 2x/week wks 16-17 (Mon + Fri), 3x from wk 18 (Mon/Wed/Fri). Never on
                # consecutive days. Heavy slow resistance: 3 s up, 3 s down, last rep hard.
                # Progress by LOAD, never by reps: 15RM in wk 16 down to 6RM by wk 20.
                #   G1 seated calf raise, bent knee — SOLEUS. The priority: running puts
                #      6-8x bodyweight through it, far more than gastroc. 4x8.
                #      Target by wk 20: 8 reps at 1.5x bodyweight (~105 kg).
                #   G2 standing calf raise, straight knee — gastroc. 4x8, single-leg when
                #      bodyweight gets easy, then weighted.
                #   G3 heel raise with the band pulling into eversion — tib post under real
                #      load, which R3 cannot reach. 3x10 slow.
                #   G4 rear-foot-elevated split squat 3x6-8 — single-leg strength and the
                #      hip control the sprain never got back.
                #   G5 Romanian deadlift 3x6 heavy — posterior chain.
                #   G6 Copenhagen plank 3x20 s/side + banded hip abduction 3x15 — glute med.
                # From wk 20, once G1-G2 are pain-free at load, add ELASTIC work: pogo hops
                # 3x20, then skipping, then low bounding. Tendon stiffness is what returns
                # energy at 3:59/km, and heavy slow work alone does not build it.
                # Secondary benefit worth more than the 215 lost km: heavy lifting above
                # ~80% 1RM improves running economy 2-8% in trained distance runners. This
                # layoff is the window to finally do it.
                # Test battery, both sides, numbers written down, repeated every Sunday:
                #   T1 single-leg heel raises to failure (height must hold) — L vs R.
                #      Benchmark is 25+; a distance runner should beat that comfortably.
                #   T2 knee-to-wall dorsiflexion in cm — L vs R
                #   T3 10 single-leg hops — pain yes/no
                # Left within 10% of right on T1 and T2 is the gate for quality work
                # returning. Until then the asymmetry IS the injury.
                15: {"Mon": ("Long run 24 km easy — wk 14's Sunday long run, run a day late",
                             "long", 24),
                     # Planned 11 km. He started, the ankle hurt from the first kilometre,
                     # and he stopped at 1.6 km. Knowing what we know now, the correct
                     # assignment for this day was zero running — so this is logged as a
                     # rest day honoured, not an 11 km session failed. The 1.6 km stays in
                     # Strava; it just is not a shortfall against anything.
                     "Tue": ("Pulled up at 1.6 km — ankle sore from the first kilometre, "
                             "so he stopped. Right call: this is where the layoff starts",
                             "rest", 0),
                     # Taken completely off — no running and no cross-training — while
                     # the ankle was still being worked out. By the 29th it was pain-free
                     # walking with stiffness only, so the rest did its job.
                     "Wed": ("FULL REST — no running, no cross-training. Ankle off "
                             "entirely", "rest", 0),
                     "Thu": ("NO RUNNING. CT2 easy spin 45 min @ 133-148 bpm + 6x1 min "
                             "high-cadence spin-ups @ 100-110 rpm, low resistance. Spin was "
                             "pain-free. PHYSIO: worth booking, no longer urgent", "rest", 0),
                     "Fri": ("NO RUNNING. CT3 bike threshold 60 min: 4x6 min @ 163-172 bpm, "
                             "3 min easy between · w/u 15 min · c/d 10 min  "
                             "+S&C upper body/core", "rest", 0),
                     "Sat": ("NO RUNNING. CT1 easy spin 45 min @ 133-148 bpm", "rest", 0),
                     # Pulled the return-to-run forward from Tue 3 Nov. Day 11, pain-free
                     # walking and a pain-free threshold bike, and with a tendon history the
                     # cost of two more rest days is higher than the risk of a 4 km jog/walk.
                     # The battery comes FIRST — it is the only objective read we have, and
                     # it is worthless once the legs are tired.
                     "Sun": ("BATTERY DONE: heel raises 30 L / 30 R, knee-to-wall 6.5 cm L / "
                             "8.0 cm R, hops pain-free both, left wobblier. RETURN TO RUN: "
                             "5 km treadmill @ 6:00/km, 0-1%. Then G4/G5/G6 — calf "
                             "calibration held back to Monday so the 24 h reaction stays "
                             "readable. DONE, ZERO PAIN: split squat 2 × 14 kg, RDL 50 kg "
                             "× 12  +M1 +R1", "recovery", 5)},
                # Graded return, every step conditional. If a gate fails, repeat the previous
                # step rather than skipping forward. No hills, no corners, no MP work.
                16: {# He says he is terrible at cycling and would rather run slowly, and a
                     # session he resents is a session that does not happen. So the two easy
                     # spins go: Monday becomes gym-only and Friday becomes a short slow run.
                     # Wednesday's bike threshold stays, and it is the LAST bike session —
                     # it is the only hard aerobic work available until running intensity
                     # returns in wk 18, and dropping it would make four straight weeks with
                     # none. Week goes 32 -> 36 km, which is the whole cost of the swap.
                     # The 24 h reaction is the real test, not the run itself: tendon pain
                     # reports late. Morning stiffness that clears in under 10 min is
                     # acceptable and expected; stiffness that lasts the morning, or any
                     # pain worse than yesterday, means repeat the previous step.
                     # NOT DONE. The calibration moves to Friday, which is now the only
                     # gym day this week.
                     "Mon": ("NO RUNNING — 24 h check was clean. GYM DID NOT HAPPEN; "
                             "calibration moved to Fri 6 Nov", "rest", 0),
                     # Second pain-free run in a row: treadmill 1 Nov, road 3 Nov. Road is
                     # a step up on surface variability from the treadmill, so this is a
                     # cleared gate, not a repeat.
                     "Tue": ("DONE, ZERO PAIN: easy 5 km flat, GT-2000. Second pain-free "
                             "run running, first on the road.  +R1", "recovery", 5),
                     "Wed": ("NO RUNNING. CT3 bike threshold 4x6 min @ 163-172 bpm, 3 min "
                             "easy between · w/u 15 min · c/d 10 min — the last bike "
                             "session  +R1", "rest", 0),
                     "Thu": ("Easy 7 km flat  +R1", "easy", 7),
                     # Monday's gym did not happen, so this is the only gym of the week and
                     # the calibration has to land here. G1 is the priority — the seated
                     # soleus number is what the wks 17-20 ladder is a percentage of. LEFT
                     # LEG FIRST, while fresh, or the injured side's number comes back
                     # corrupted by fatigue. G4/G6 drop this week: they were done Sun 1 Nov
                     # and finding the calf number matters more than a second exposure.
                     # DONE. Calibration attempted and NOT usable: standing single-leg
                     # bent-knee raise gave 10 L then 15 L on a second attempt, 15 R. A
                     # fatigued leg does not gain 50%, so the first was a cold unfamiliar
                     # movement. Video confirmed technique is sound — wall for balance, free
                     # foot in the air, knee bend held. But he cannot drop the heel below
                     # the step: the knee-over-toes position spends his dorsiflexion before
                     # the heel descends, so the test measured ankle range, not soleus.
                     # Recalibrate SEATED on Mon 9 Nov. No capacity deficit found.
                     "Fri": ("DONE: easy 4 km, then gym — calf work, G2, G3, G5 RDL, G4/G6. "
                             "Calibration not usable (bottomed out on dorsiflexion, not "
                             "strength); moved to Mon 9 Nov, seated  +R1",
                             "recovery", 4),
                     # Left ANKLE JOINT stiffness on Sat morning — not calf DOMS, not
                     # pain. First reaction since the return, and it follows Friday's gym.
                     # Prime suspect is the standing knee-over-toes raise: repeated
                     # end-range joint loading, to failure, on a joint that is already
                     # restricted. That movement is OUT until this settles; Monday's seated
                     # calibration does not load the joint at end range, so it stands.
                     # Per the gate, repeat a cleared step rather than progress: 8 -> 5.
                     # DONE. Treadmill at the gym plus the cut-down non-calf gym session
                     # (G3, G5, G6, core, R1 isometrics). No calf raises, no G4.
                     "Sat": ("DONE: easy 5 km flat — CUT FROM 8 after left ankle joint "
                             "stiffness. Non-calf gym only: G3, G5, G6, R1. No standing "
                             "knee-over-toes raises  +R1", "easy", 5),
                     # DONE, ZERO PAIN, and at the FULL 12 — I argued for 9 on the grounds
                     # that 5 -> 12 the day after a joint reaction was too big a step. He
                     # took the 12 and it was clean. Longest run since the 27 Oct abort
                     # (1.61 km) and the sixth consecutive pain-free run. That dates
                     # Saturday's stiffness to Friday's gym work, not to the tendon
                     # progressing — the standing knee-over-toes raise is the culprit and
                     # stays out. Return-to-run ladder is complete: wk 17 runs as written.
                     # Test battery NOT recorded — knee-to-wall still outstanding, and it
                     # is the number the wks 18-20 ramp decision needs.
                     "Sun": ("DONE, ZERO PAIN: easy 12 km flat at the full planned "
                             "distance. Longest since the abort. Test battery not "
                             "recorded — knee-to-wall still owed  +R1",
                             "long", 12)},
                # Rebuild after the layoff. Quality comes back one session at a time:
                # wk 17 none, wk 18 one threshold, wk 19 threshold + a short MP block, wk 20
                # back to normal. Nothing with hills or sharp cornering until wk 19 — those
                # load the subtalar joint hardest. BJJ drills stay out until wk 19.
                17: {# CALIBRATION, moved here from wk 16 and redesigned. The standing
                     # knee-over-toes version bottoms out on his dorsiflexion, not his
                     # soleus — he physically cannot drop the heel below the step (6 Nov
                     # video). Seated removes the confound: knee flexed to 90 deg with the
                     # shin VERTICAL biases soleus without spending any ankle range.
                     # DONE 9 Nov and it worked, third time: 35 kg dumbbell on the thigh,
                     # 15 reps EACH leg at tempo, 2-3 in reserve on both. The number is a
                     # floor, not a 15RM - the setup caps out near 40 kg, so the true max
                     # was never reached and the percentage ladder is retired in favour of
                     # real kilos on a double progression. Equipment is now the limiter:
                     # wk 19 onward needs a barbell across the thighs or a leg press.
                     # LEFT ANKLE STIFF AFTERWARDS - second reaction in four days, both
                     # after loaded calf raises. See the load-ladder note: the common
                     # factor is the heel dropping below the forefoot, i.e. loaded
                     # end-range dorsiflexion, not the knee angle. Left side is now TOP
                     # HALF ONLY on G1 and G2.
                     "Mon": ("DONE: rest from running. GYM — G1 SEATED CALF CALIBRATION "
                             "landed: 35 kg × 15 EACH LEG at 3 s up / 3 s down, 2-3 reps in "
                             "reserve. No side-to-side difference. LEFT ANKLE STIFF AFTER — "
                             "left leg goes TOP-HALF-ONLY from here. Then G2-G6  +R1",
                             "rest", 0),
                     "Tue": ("Easy 8 km flat — first full week back, no quality at all. "
                             "Running has been clean for 6 runs; the reactions are coming "
                             "from the GYM, not the runs, so this stands", "easy", 8),
                     "Wed": ("Easy 7 km flat", "easy", 7),
                     "Thu": ("Easy 9 km flat — no hill sprints this block", "easy", 9),
                     "Fri": ("Recovery 5 km easy  +GYM G1-G6  +R1", "recovery", 5),
                     "Sat": ("Easy 7 km + 4×20s strides — first strides back, on the flat",
                             "easy", 7),
                     "Sun": ("Easy 10 km — rebuilding the long run from a low base", "long", 10)},
                # MECHANISM CORRECTED 9 Nov from the HealthFit FIT files. The onset was
                # NOT the 24 Oct hilly 7 km; it was the 22 Oct session, 2x5 km @ 3:54/3:55
                # on a FLAT route with no recorded ascent. The laps show why: ground
                # contact fell to 185-187 ms against 209-224 ms on his easy runs, and step
                # length rose to 1362 mm against ~1150. Short stance + long stride at speed
                # is peak Achilles force and peak loading rate, held for 10 km. Cadence was
                # never the problem (175-186 spm throughout, already high) and neither was
                # climbing. So SPEED EXPOSURE is the thing to stage carefully, and easy
                # volume is the cheap part: the 24 km on 26 Oct and the 19 km on 18 Oct both
                # ran at 212-224 ms stance, i.e. low loading rate, and were tolerated.
                # Week 18 therefore keeps its quality session in full. Short reps with
                # full recoveries are the lowest-exposure way back into speed - 4 km of
                # fast running in 1 km chunks, against the 10 km continuous block that
                # caused this.
                # EASY VOLUME RESTORED 9 Nov. It was briefly cut to 55, which was paying
                # twice for one risk: if easy running at 212-224 ms stance is what he
                # tolerated through 19 km and 24 km, then cutting it buys little and costs
                # the aerobic rebuild. 60 and 74 are both at or below his best week on
                # record (76.1, wk 9), so wks 18-19 reclaim ground rather than set records.
                # The speed cuts stand - that is where the risk actually lives.
                18: {"Mon": ("Rest from running  +GYM G1-G6  +R1", "rest", 0),
                     "Tue": ("Threshold: 4×1 km @ 3:50/km, 90s jog @ 6:00/km · w/u 3 km · "
                             "c/d 2 km — first quality since the injury, half the usual volume, "
                             "flat loop only. SHORT reps on purpose: 1 km chunks, not blocks", "quality", 12),
                     "Wed": ("Easy 9 km  +GYM G1-G6", "easy", 9),
                     "Thu": ("Easy 10 km", "easy", 10),
                     "Fri": ("Recovery 6 km easy — 5:35-6:05/km, HR under 140, slower than "
                             "you think  +GYM G1-G6  +R1", "recovery", 6),
                     "Sat": ("Easy 8 km + 6×20s strides", "easy", 8),
                     "Sun": ("Long 15 km easy", "long", 15)},
                19: {"Mon": ("Rest from running · BJJ drills/technical, no live rounds  "
                             "+S&C (easy-day session) — BJJ returns here if the ankle has been "
                             "clean for three weeks", "rest", 0),
                     # As written this week asked for 12.5 km of running faster than 4:10
                     # across two sessions, three weeks after a 10 km fast block put him
                     # out for three. Cut to 9 km of fast work: 4x1.5 km instead of 5, and
                     # the first MP block is 3 km, not 5. The 20 km Sunday is UNTOUCHED -
                     # slow long runs are not what hurt him and the aerobic rebuild needs
                     # it. Week total HELD at 74: the 3 km taken off the quality days
                     # goes back onto the easy days rather than out of the week.
                     "Tue": ("Threshold: 4×1.5 km @ 3:50/km, 75s jog @ 6:00/km · w/u 3 km · "
                             "c/d 2 km — CUT FROM 5×1.5 and 3:48", "quality", 11),
                     "Wed": ("Easy 12 km + 6×20s strides  +GYM G1-G6", "easy", 12),
                     "Thu": ("Medium-long 13 km w/ middle 3 km @ MP — first marathon-pace work "
                             "back, CUT FROM 5 km. Continuous fast blocks are the shape that "
                             "injured him, so this one stays tiny", "quality", 13),
                     "Fri": ("Recovery 8 km easy — 5:35-6:05/km  +BJJ (drills only — no live "
                             "rounds)", "recovery", 8),
                     "Sat": ("Easy 10 km + strides", "easy", 10),
                     "Sun": ("Long 20 km easy", "long", 20)},
                # Week 20 was the single riskiest week in the plan: Thursday asked for
                # 3x4 km @ MP, i.e. 12 km of marathon-pace running, MORE than the 10 km
                # that injured him, in the same week as a 6x1000 VO2 session. Now 9 km of
                # MP in 3 km blocks and 5x1000.
                # Volume lands at 80 - not the original 85, and not the 76 it was briefly
                # cut to. 85 would be a 12% lifetime high the week before the Sevilla
                # Half, five weeks out of a layoff, with the left ankle still 2.5 cm down
                # on the right: too many ands at once. 80 is a +4 km high over wk 9's
                # 76.1, which is an ordinary progression, and it keeps the robustness
                # argument intact.
                20: {"Mon": ("Rest from running · BJJ drills/technical, no live rounds  "
                             "+GYM G1-G6  +R1", "rest", 0),
                     "Tue": ("VO2: 5×1000 m @ 3:26/km, 2:30 jog @ 6:00/km · w/u 3.5 km · "
                             "c/d 2 km — CUT FROM 6 reps", "quality", 13),
                     "Wed": ("Easy 11 km + 6×20s strides  +GYM G1-G6", "easy", 11),
                     "Thu": ("MP tempo: 3×3 km @ MP, 2 min float @ 4:28/km · w/u 2 km · "
                             "c/d 1 km — CUT FROM 3×4 km. 9 km of MP, still under the 10 km "
                             "block that caused the injury", "quality", 13),
                     "Fri": ("Recovery 8 km easy — 5:35-6:05/km  +BJJ (drills only — no live "
                             "rounds)  +GYM G1-G6  +R1", "recovery", 8),
                     "Sat": ("Easy 7 km + strides", "easy", 7),
                     "Sun": ("28 km easy — steady week, race is next Sunday", "long", 28)},
                26: {"Wed": ("Easy 20 km + 6×20s strides  (double: split AM/PM)", "easy", 20),
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
# Wks 18-20 restaged 9 Nov: the SPEED is cut, the mileage is not. The ramp runs
# 35 -> 46 -> 60 -> 74 -> 80, against 35 -> 46 -> 60 -> 74 -> 85 originally. Only
# wk 20 moves on volume, and only because 85 would be a 12% lifetime high.
VOL_OVERRIDE = {9: 57, 11: 57, 12: 63, 13: 69, 16: 33, 20: 80, 21: 68, 26: 95}

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

# ---- Left ankle rehab, Nov 2026. Two tendon episodes in this leg in eight months
# (achilles musculotendinous junction in March, medial ankle in October) on top of a
# 2018 football sprain. That is a capacity deficit, so the ankle gets loaded rather
# than rested. Split by load, because tendon collagen synthesis runs net-negative for
# 24-36 h after a heavy session and only turns positive again around 48-72 h: the low
# load work is daily, the heavy work is twice a week and never on back-to-back days.
# ---- BATTERY, 1 Nov 2026 (baseline). T1 heel raises to failure 30 L / 30 R. T2
# knee-to-wall 6.5 cm L / 8.0 cm R. T3 ten hops, no pain either side, left wobblier.
# That rewrites the diagnosis. 30/30 is symmetrical and above the 25-rep benchmark, so
# the capacity-deficit reading was wrong: calf ENDURANCE is not the problem. The problem
# is dorsiflexion. Normal is 9-12 cm; both his ankles are restricted and the left is 19%
# worse. A tibia that cannot travel forward over the foot has to find the range somewhere,
# and where it finds it is pronation through the subtalar joint — precisely where the pain
# is. It also explains the 24 Oct outlier: 118 m of climb over 7 km is the highest
# dorsiflexion demand in running, asked of a 6.5 cm ankle for an hour.
# So mobility leads the rehab now and the calf ladder is demoted from the treatment to
# useful supporting work. One caveat kept in view: 30 reps is an ENDURANCE test, not a
# strength test, so the seated-calf 15RM is still worth knowing before fully letting go
# of the strength story.
REHAB_MOBILITY = [
    ["Banded talar glide (M1)", "3 × 10 / side, 2× daily", "THE priority. Heavy band round the "
     "ankle just below the bony bumps, anchored in front, pulling the ankle bone backwards "
     "while you drive the knee over the toes. Heel stays down. Targets the joint restriction "
     "the 2018 sprain left — stretching does not reach it"],
    ["Knee-to-wall rocks (M2)", "3 × 10 / side, 2× daily", "Same position as the test, rocking "
     "into the end range. Cheap, do it anywhere, do it often"],
    ["Soleus stretch, knee bent (M3)", "3 × 45s / side", "Bent knee or it becomes a gastroc "
     "stretch. Secondary to M1 — if the block is in the joint, stretching the muscle is "
     "treating the wrong tissue"],
    ["Re-test knee-to-wall", "Weekly, Sunday", "The target is left matching right AND both "
     "past 9 cm. This number, not how the ankle feels, is the gate for hills returning"],
]

REHAB_DAILY = [
    ["Isometric calf hold (R1)", "5 × 45s / leg", "Mid-range, ~70% effort. Daily, run days "
     "included — loads the tendon with almost no recovery cost"],
    ["Banded resisted inversion (R3)", "3 × 15 slow", "Tib posterior, light load"],
    ["Single-leg balance, eyes closed (R4)", "3 × 30s", "Aimed at the 2018 sprain, not the tendon"],
    ["Short foot / toe yoga (R5)", "3 × 10", "Intrinsics — the foot's own suspension"],
    ["Test battery", "Every Sunday", "Heel raises to failure, knee-to-wall in cm, 10 single-leg "
     "hops — left vs right, written down. Left within 10% of right is the gate for quality work"],
]
# Loads are starting estimates for ~70 kg bodyweight, not prescriptions. Calibrate on
# session one against the rep target: the last rep must be hard and the tempo must hold.
# If the bar moves faster than 3 s up / 3 s down it is too light, whatever the number says.
REHAB_GYM = [
    ["Seated calf raise — SOLEUS (G1)", "3×15 → 4×6 / LEG", "One leg at a time. THE priority: running drives 6-8× "
     "bodyweight through soleus and only a bent knee loads it. 3 s up, 3 s down. "
     "LEFT LEG: TOP HALF ONLY — heel stops level with the forefoot, never below it. "
     "Right leg full range"],
    ["Standing calf raise — gastroc (G2)", "3×15 → 4×6", "SINGLE LEG AND LOADED from day one. "
     "Bodyweight is ~1× at the ankle against 6-8× in running, so it is a warm-up, not a "
     "stimulus. Same tempo. LEFT LEG: TOP HALF ONLY, same rule as G1. "
     "No bent-knee, knee-over-toes version on either side"],
    ["Heel raise vs band into eversion (G3)", "3 × 10 slow", "Light → heavy band. Tib post under "
     "real load, which the daily band work cannot reach"],
    ["Rear-foot-elevated split squat (G4)", "3 × 8 → 3 × 6 / leg", "Bodyweight → 2 × 20 kg DBs. "
     "Single-leg strength and the hip control the sprain took away"],
    ["Romanian deadlift (G5)", "3 × 6", "40 → 80 kg. Posterior chain. 3 s lower"],
    ["Copenhagen plank + banded hip abduction (G6)", "3 × 20s/side + 3 × 15", "20s → 40s. Glute med"],
    ["Pogo hops, then skipping, then low bounding", "3 × 20 — from wk 20 only", "Heavy slow work "
     "builds a strong tendon, not a stiff one, and stiffness is what returns energy at 3:59/km"],
]
# Single-leg bodyweight raises are easy for him (1 Nov), which was predictable and makes
# the first two rungs of the old ladder worthless: bodyweight loads the achilles at ~1x
# bodyweight and running drives 6-8x. So the ladder no longer starts from a number guessed
# off his bodyweight. Session one is a CALIBRATION: find the load he can just manage for 15
# at 3 s up / 3 s down, and every later week is a percentage of that. Percentages travel;
# guessed kilos do not.
REHAB_LOADS = [
    ["Wk 16", "3 × 15", "— standing calibration failed twice", "2 × 14 kg (done 1 Nov)",
     "50 kg (done 1 Nov)"],
    ["Wk 17", "4 × 12", "35 kg — DONE 9 Nov, 15/leg with 2-3 in reserve",
     "2 × 18 kg", "60 kg"],
    ["Wk 18", "4 × 10", "40 kg — the dumbbell-on-thigh ceiling", "2 × 22 kg", "67 kg"],
    ["Wk 19", "4 × 8", "47 kg — NEEDS a barbell or leg press", "2 × 26 kg", "73 kg"],
    ["Wk 20", "4 × 6", "54 kg = 1.5× bodyweight benchmark", "2 × 30 kg", "80 kg"],
]
REHAB_SCHEDULE = [
    ["Wks 16-17", "Mon + Fri", "Rebuild. Calibrate, then climb the ladder"],
    ["Wks 18-20", "Mon + Wed + Fri", "The window with room for three — volume is still moderate"],
    ["Wk 21", "Mon only", "Sevilla on the Sunday. Nothing heavy after Monday"],
    ["Wks 22-23", "Mon + Wed + Fri", "Back to three"],
    ["Wks 24-30", "Mon + Fri", "Peak block, 95-116 km/wk. Drop to 3×5 heavy and low volume: "
     "the job here is holding the strength you built, not adding to it. Three heavy "
     "sessions on top of peak mileage is how strength work starts causing injuries "
     "instead of preventing them"],
    ["Wk 26", "Mon only", "Race on the Sunday"],
    ["Wks 31-32", "Mon only", "Taper. Maintenance, no plyometrics"],
    ["Wk 33", "None", "Race week. Nothing heavy inside 5-7 days of Tokyo"],
]
REHAB_BLOCKS = [
    {"title": "Ankle mobility — the priority after the 1 Nov battery",
     "headers": ["Drill", "Dose", "Why"],
     "note": "Battery 1 Nov: heel raises 30 left / 30 right — symmetrical and strong, which "
             "rules the strength story out. Knee-to-wall 6.5 cm left / 8.0 cm right against a "
             "9-12 cm norm — restricted both sides, 19% worse on the left. Range the ankle "
             "cannot produce gets borrowed from the subtalar joint, which is where the pain is. "
             "This block is now the actual treatment.",
     "rows": REHAB_MOBILITY},
    {"title": "Left ankle — daily, 8 min", "headers": ["Exercise", "Sets × Reps", "Cue / why"],
     "note": "Every day including run days. Low load by design: this is what keeps the tendon "
             "working between the heavy sessions, and none of it costs recovery.",
     "rows": REHAB_DAILY},
    {"title": "Gym — heavy slow resistance · runs to Tokyo",
     "headers": ["Exercise", "Sets × Reps", "Load and why"],
     "note": "DEMOTED by the 1 Nov battery — 30/30 heel raises means this is no longer the fix, "
             "it is supporting work, and mobility comes first. Still worth doing properly: the "
             "economy gain is real and 30 reps proves endurance, not strength. Never on "
             "consecutive days. Progress by LOAD, never by reps — 15RM in wk 16 down to "
             "6RM by wk 20. Adding reps instead of plates turns tendon rehab into cardio. The "
             "side benefit is worth more than the 215 km this injury cost: heavy lifting above "
             "~80% 1RM improves running economy 2-8% in trained distance runners.",
     "rows": REHAB_GYM},
    {"title": "Gym through to Tokyo — how the dose changes",
     "headers": ["Weeks", "Sessions", "Why"],
     "note": "The ankle work does not stop when the injury settles — that is exactly the "
             "mistake that turned March into October. What changes is the dose, not whether "
             "it happens. The hips and posterior chain (G4-G6) run the whole way on the same "
             "schedule; they are what keeps the ankle from having to cover for anything else.",
     "rows": REHAB_SCHEDULE},
    {"title": "The load ladder, week by week",
     "headers": ["Week", "Reps (calves)", "Calf load", "G4 split squat", "G5 RDL"],
     "note": "CALIBRATED 9 Nov, and the percentage ladder is retired. Seated, shin vertical, "
             "35 kg dumbbell on the thigh: 15 reps on EACH leg at 3 s up / 3 s down, with 2-3 "
             "reps still in reserve on both. So the true 15RM is above 35 kg and was never "
             "found — the dumbbell-on-thigh setup runs out of road around 40 kg, which is the "
             "ceiling flagged before the session. Percentages of an unfound maximum are "
             "useless, so the Calf load column is now real kilos on a double progression: hold "
             "the rep target, and add load as soon as you clear it on BOTH legs with the tempo "
             "intact. THE EQUIPMENT IS NOW THE BINDING CONSTRAINT. His gym has no seated calf "
             "machine, and from wk 19 the prescription exceeds what balances on a thigh — it "
             "needs a barbell across the thighs on a pad, or a single-leg calf press on a leg "
             "press. Find one before wk 19 or the ladder stalls at 40 kg. "
             "RANGE RESTRICTED ON THE LEFT, 10 Nov, after a SECOND joint reaction. The left "
             "ankle went stiff after the 6 Nov standing calf raises and again after the 9 Nov "
             "seated ones. On 7 Nov that was blamed on the knee-over-toes position spending "
             "his dorsiflexion, and the seated version was designed to avoid it — but the "
             "seated version provoked it too, so that reasoning was wrong. What both setups "
             "share is the BOTTOM of the rep: the heel drops below the forefoot, which is "
             "loaded end-range dorsiflexion whatever the knee is doing. With 7.5 cm of range "
             "on that side, every rep bottoms out at his limit, 15 times, under 35 kg. "
             "So the fix is to cut the RANGE, not the load: left leg stops at neutral, heel "
             "level with the forefoot, top half of the movement only. Right leg has 10 cm and "
             "keeps full range. Reduced-range loading is a recognised way to keep a tendon "
             "stimulus while avoiding a provocative position, and it costs almost nothing here "
             "because there is no capacity deficit to chase. "
             "This reaction pattern is itself diagnostic: pain and stiffness provoked by "
             "loaded end-range dorsiflexion, on the restricted side only, is the textbook "
             "presentation of anterior ankle impingement. It is what the lateral X-ray view "
             "would show, and it is now shaping his training week by week, which makes the "
             "1 Dec appointment too late to be useful. "
             "THIRD CONFIRMATION OF NO CAPACITY DEFICIT: 30/30 straight-knee raises (1 Nov), "
             "15/15 bent-knee bodyweight (6 Nov), 15/15 at 35 kg seated (9 Nov). He reports the "
             "right FEELING stronger, but nothing measurable separates them across three tests. "
             "This is not a strength problem and never was — it is a joint range problem "
             "(7.5 cm left vs 10.0 right, 8 Nov), which is what the imaging is for. "
             "1 Nov actuals: split squat 2 × 14 kg and RDL 50 kg for 12 clean reps, both beating "
             "the estimate, so the RDL ladder is built off an implied 6RM near 60 kg. The CALF "
             "loads are ONE LEG AT A TIME — two-leg lets the strong side quietly carry the weak "
             "one, which is how he got here. The wk 20 target of ~54 kg per leg is the 1.5× "
             "bodyweight benchmark, since both legs together would be ~105 kg.",
     "rows": REHAB_LOADS},
]

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

# The ankle work runs to Tokyo, not just through the comeback. The DOSE changes though:
# three heavy sessions a week is right while volume is moderate and wrong at 110-116 km,
# and nothing heavy goes near a race week. Stamped onto the days rather than hand-written
# into each note, because "every week" only survives if nothing has to be remembered.
#   wks 16-17  Mon + Fri          rebuilding, 2x
#   wks 18-20  Mon + Wed + Fri    the window with room for 3x
#   wk  21     Mon only           Sevilla on the Sunday
#   wks 22-23  Mon + Wed + Fri    back to 3x
#   wks 24-30  Mon + Fri          peak block: maintain strength, add no fatigue (3x5 heavy)
#   wks 31-32  Mon only           taper, maintenance, no plyometrics
#   wk  33     none               race week
RACE_WEEKS = (21, 26, 33)

def gym_for(w):
    if w == 33:         return (), ""
    if 31 <= w <= 32:   return ("Mon",), "GYM maintenance only — 3x5, no plyometrics"
    if w in RACE_WEEKS: return ("Mon",), "GYM G1-G6 light — race on Sunday"
    if 24 <= w <= 30:   return ("Mon","Fri"), "GYM G1-G6 maintenance — 3x5 heavy, low volume"
    if 18 <= w <= 23:   return ("Mon","Wed","Fri"), "GYM G1-G6"
    return ("Mon","Fri"), "GYM G1-G6"

def _stamp_rehab(w, days):
    gym_days, gym_txt = gym_for(w)
    # Mobility stays twice daily while the dorsiflexion deficit is being closed, then
    # drops to once a day as maintenance. The isometrics fold into the gym work once the
    # heavy calf loading is established.
    tail = ("  +M1/M2 mobility (2x daily) +R1 isometrics" if w <= 20
            else "  +M1/M2 ankle mobility (daily)")
    for dow in DOW:
        txt, typ, km = days[dow]
        if "+M1" in txt or "+M1/M2" in txt:
            continue
        for junk in ("  +S&C (easy-day session)", "  +S&C (hard-day session)",
                     "  +light S&C (taper)", "  +R1", " +R1"):
            txt = txt.replace(junk, "")
        txt = txt.rstrip()
        if dow in gym_days and "+GYM" not in txt:
            txt += "  +" + gym_txt
        days[dow] = (txt + tail, typ, km)
    return days


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
    # Wks 16-20 carry the ankle rehab every single day, run days included. Stamping it
    # here rather than writing it into each note is the only way it does not get dropped
    # from half of them: "daily" has to mean daily or the mobility work does nothing.
    if w >= 16:
        days = _stamp_rehab(w, days)
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
            "intro": "Rotating rather than wearing one pair out is the point — varying the "
                     "loading pattern is associated with materially lower injury risk, and that "
                     "matters more at 90-116 km/wk than which model you pick. The GT-2000 15 "
                     "(new, 30 Oct) and the Clifton 9 (447 km) carry the comeback between them. "
                     "Mileage below is counted off the plan, not typed in. Five pairs to the "
                     "start line. Rotating rather than "
                     "wearing one pair out is the point — varying the loading pattern is "
                     "associated with materially lower injury risk, and that matters more at "
                     "90-116 km/wk than which model you pick. Every session on the plan is "
                     "tagged with its shoe.",
            "headers": ["Shoe", "Used for", "km from here", "Total at Tokyo", "Status"],
            "rows": shoe_rows(),
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
        "strength": C.strength("1–13", "14–30", football=False, rehab=REHAB_BLOCKS),
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
    "gt2000":  "GT-2000 15",
    "clifton": "Clifton 9",
    "daily2":  "Daily trainer #2",
    "long":    "Max-cushion (long-run)",
    "machx":   "Mach X3",
    "evosl":   "EVO SL",
    "quality2": "Quality trainer #2",
    "race":    "RACE SHOE",
}
# Odometer at 1 Nov 2026, from Strava gear. The GT-2000 arrived on 30 Oct for the
# return from the ankle injury and is the only pair with life in it.
SHOE_KM_NOW = {"gt2000": 0, "clifton": 447, "machx": 245, "evosl": 511, "daily2": 0,
               "long": 0, "race": 0, "quality2": 0}
# A trainer is done around 600-800 km depending on the foam; the EVO SL's unplated
# Lightstrike Pro packs out early, which is why it retires first and why it stopped
# being an easy-run shoe on 26 Oct.
SHOE_RETIRE = {"gt2000": 700, "clifton": 600, "machx": 550, "evosl": 550,
               "daily2": 700, "long": 700, "quality2": 550}
# The EVO SL stops at Sevilla, not Tokyo. Counting the plan rather than guessing put it
# at 610 km by March, 60 past the point its unplated Lightstrike Pro is worth running on
# — and it is already the pair implicated in carrying the October ankle injury. A second
# quality pair takes its slot from wk 22 so the Mach X also stays inside its own limit.
EVOSL_LAST_WEEK = 21
# The racer only comes out for the two races and the handful of MP sessions that
# bed it in — it holds its bounce for ~250-300 km and must not be spent on training.
# One bed-in run before each race. Wk 18 rather than 19 so there is a week in hand
# to react if the shoe does not suit. Wk 29 rather than 30 before Tokyo: 29 is the
# dress rehearsal (35 km with 12 km @ MP) and 30 is an easy run, so 29 is the one
# that actually rehearses race pace in race shoes.
RACE_SHOE_DAYS = {(18,"Sun"), (21,"Sun"), (29,"Sun"), (33,"Sun")}
# The Clifton is already on 447 km, so it is the pair that runs out first: it takes
# half the easy running through the rebuild and hands over to the second new trainer
# at wk 20, by which point it is near 600 km and done.
DAILY2_FROM = 20
# Long runs stay in the daily trainers while they are short. The max-cushion pair is
# only worth buying once the long run is actually long, which is wk 20 onward.
LONG_SHOE_FROM = 20

def shoe_for(w, dow, typ, sess):
    if typ == "rest":
        return None
    if (w, dow) in RACE_SHOE_DAYS:
        return SHOES["race"]
    if typ in ("race",):
        return SHOES["race"]
    if typ in ("quality", "tt"):
        # Weighted toward the Mach X3: it starts the block on 245 km against the
        # EVO SL's 511, and the EVO SL is a racer-trainer that should be retired
        # around 550 km rather than run into the ground through the peak weeks.
        if w <= EVOSL_LAST_WEEK:
            return SHOES["evosl"] if w % 3 == 0 else SHOES["machx"]
        return SHOES["quality2"] if w % 2 == 1 else SHOES["machx"]
    if typ == "long" and w >= LONG_SHOE_FROM:
        return SHOES["long"]
    # Easy, recovery and the short rebuild long runs share two daily trainers. Through
    # the comeback that is the new GT-2000 and the Clifton; the Clifton hits ~600 km
    # around wk 20 and the second new trainer takes its slot from there.
    # Wks 16-17 are the comeback and they all go in the GT-2000: it is new, it is the
    # stability pair bought for this ankle, and rotating a 447 km Clifton back in during
    # a return from injury is the wrong way round. The Clifton rejoins at wk 18.
    if w <= 17:
        return SHOES["gt2000"]
    second = SHOES["daily2"] if w >= DAILY2_FROM else SHOES["clifton"]
    return second if (w % 2 == 1 or typ == "recovery") else SHOES["gt2000"]


def shoe_rows(from_week=16):
    """Rows for the Shoes table, counted off the plan rather than typed by hand.
    Hand-typed mileage is how a rotation quietly drifts out of date — and most
    worn-shoe injuries happen because nobody was counting."""
    km = {k: 0.0 for k in SHOES}
    name_to_key = {v: k for k, v in SHOES.items()}
    for w in range(from_week, 34):
        for dow, (txt, typ, d) in build_week(w).items():
            sh = shoe_for(w, dow, typ, txt)
            if sh:
                km[name_to_key[sh]] += d
    use = {
        "gt2000":  "Easy + recovery, and the comeback runs",
        "clifton": "Easy + recovery until it runs out",
        "daily2":  "Easy + recovery from Wk 20",
        "long":    "Every long run from Wk 20",
        "machx":   "Most quality sessions",
        "evosl":   "Quality every third week, until Sevilla",
        "quality2": "Quality, alternating, from Wk 22",
        "race":    "Sevilla, Tokyo + 2 bed-in runs",
    }
    buy = {
        "gt2000":  "Owned — new on 30 Oct, 0 km",
        "clifton": "Owned — 447 km. Retire around 600.",
        "daily2":  "Early Jan, as the Clifton runs out",
        "long":    "Before Wk 20 — soft and high-stack (Nimbus / Skyflow / Kiprun KS900)",
        "machx":   "Owned — 245 km",
        "evosl":   "Owned — 511 km. RETIRE AFTER SEVILLA, not Tokyo.",
        "quality2": "Early Dec — replaces the EVO SL (Mach X 3 again, or similar)",
        "race":    "Early-mid Nov — Metaspeed Sky / Alphafly 3 / Adios Pro 5",
    }
    rows = []
    for k in ("gt2000", "clifton", "daily2", "long", "machx", "evosl", "quality2", "race"):
        total = SHOE_KM_NOW.get(k, 0) + km[k]
        flag = ""
        lim = SHOE_RETIRE.get(k)
        if lim and total > lim:
            flag = f" ⚠ {int(total - lim)} km past its limit"
        rows.append([SHOES[k], use[k], str(int(round(km[k]))), f"{int(round(total))}{flag}", buy[k]])
    return rows


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
