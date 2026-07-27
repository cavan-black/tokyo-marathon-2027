"""Japan trip itinerary — Tokyo (race week incl. Ghibli Museum, snow monkeys, Shibuya/
Harajuku/teamLab/go-karting all moved to before the race, Golden Gai moved to after it),
a 2-day Nakasendo Trail (Magome-Tsumago) between Tokyo and Kyoto, Kyoto/Nara (incl. a
Fushimi sake brewery, a Yamazaki whisky day, and Ichijoji Sagarimatsu doubling as the
transfer to Osaka), Osaka (Haru Basho sumo, NPB baseball and boat racing spread one per
day, with the last day's evening folded straight into the Niseko transfer), Niseko,
Sapporo, Miyazaki (Kyushu) on the way south, then Okinawa. build() -> trip dict.

Route (27 Feb - 27 Mar 2027, 29 days): Tokyo race week (Ghibli Museum, snow monkeys day
trip, and Shibuya/Harajuku/teamLab/go-karting all stacked onto 1 March, 6 days clear of
the race) -> RACE -> Golden Gai that evening -> 2 days on the Nakasendo Trail (Tokyo ->
Magome -> Tsumago walk -> Kyoto) -> 4 days Kyoto/Nara (Fushimi Inari + sake brewery,
Yamazaki Distillery whisky day trip, Nara/Omizutori, then Gion/Kiyomizu-dera/Ichijoji
Sagarimatsu doubling as the Osaka transfer — leave Kyoto that evening, arrive Osaka late)
-> 3 days Osaka (Haru Basho sumo, NPB baseball and Boat Race Suminoe spread one per day
instead of stacked on the last one, freeing that evening for an early, direct transfer
to Niseko rather than a dedicated travel day) -> Niseko -> Sapporo (1 night) -> Miyazaki
(2 days) -> Okinawa (Naha/Kerama, 4 nights) -> home direct from Naha.

This itinerary has been reworked several times in the same places, so worth tracking the
net effect rather than each individual change: Nakasendo went 2 -> 3 days (a rest day
added post-marathon) -> back to 2 (freed up again, on request, since the point was to
free a day rather than spend it here). Kyoto/Nara went 3 -> 5 days (Ichijoji + Arima
Onsen added) -> 4 (Arima Onsen dropped entirely; Ichijoji now doubles as the Osaka
transfer instead, saving the day Arima Onsen would have used). Osaka's sumo/baseball/
boat racing were stacked on one day, then spread across all three specifically so the
last evening could be freed for the Niseko transfer, eliminating the old dedicated "To
Niseko" travel day. Whisky was swapped for Arima Onsen, then brought back as its own day
(Arima Onsen has since been dropped instead, so whisky is the one that stuck). Ishigaki
was dropped from the route entirely. Sapporo went from 2 nights to 1, Miyazaki from 3
days to 2. Net effect on the trip length across ALL of this: 33 (original) -> 37 (peak,
mid-additions) -> 31 -> 32 -> 29 (this round: Nakasendo -1, Kyoto/Nara -1, "To Niseko"
folded into Osaka -1) — 4 days shorter than the original 33, even after everything added
along the way."""
from datetime import date


def d(y, m, dd):
    return date(y, m, dd).isoformat()


def build():
    legs = [
        {"name": "Travel out", "blurb": "Depart & fly to Japan.", "days": [
            {"date": d(2027, 2, 27), "title": "Depart for Japan",
             "detail": "Long-haul out — arrive the next day depending on route.", "tag": "travel"},
        ]},
        {"name": "Tokyo — race week", "blurb": "A full week based in Tokyo before the race — settle in, "
                                                 "explore properly, no rushing.", "days": [
            {"date": d(2027, 2, 28), "title": "Arrive & settle",
             "detail": "Land, transfer into Tokyo, check in. Easy walk only — race is 7 days out.", "tag": "travel"},
            {"date": d(2027, 3, 1), "title": "Asakusa, Shibuya, Harajuku, teamLab & go-karting",
             "detail": "Daytime: Senso-ji temple, Nakamise shopping street, Sumida river walk in Asakusa, then "
                       "across town to Shibuya Crossing and Harajuku's Takeshita Street. In the evening: "
                       "teamLab (Planets or Borderless) if tickets allow, then real-life Mario Kart — "
                       "public-road go-karting through Tokyo in costume (the original \"MariCAR\" brand was "
                       "sued by Nintendo and rebranded, now mainly trading as \"Street Kart\"; costumes are no "
                       "longer Nintendo characters but the karting itself is the same). SORT BEFORE YOU FLY: "
                       "you need an International Driving Permit (1949 Geneva Convention) arranged in your "
                       "home country before departure — this can't be sorted in Japan, same category of hard "
                       "deadline as the Ghibli tickets. A genuinely big day, but it's deliberately on the "
                       "Monday: 6 days clear of the race, so there's no need to hold back — that's exactly why "
                       "it's stacked here rather than closer to race day. (Golden Gai's moved to after the "
                       "race instead — better suited to a proper celebration than a school-night pre-race "
                       "outing.)", "tag": "city"},
            {"date": d(2027, 3, 2), "title": "Snow monkeys — Jigokudani, Nagano",
             "detail": "Jigokudani Monkey Park (Yudanaka): wild Japanese macaques bathing in hot springs, one of "
                       "Japan's most famous wildlife sights. Hokuriku Shinkansen Tokyo→Nagano (~1h20-1h30), then "
                       "the Nagano Dentetsu line to Yudanaka (~45min-1h), then a short bus/taxi + ~30 min forest "
                       "walk to the park. A long day (~10-12h door to door) but a genuine highlight, and a good "
                       "low-intensity day the morning after a big night out. Race is still 5 days out.",
             "tag": "tourist"},
            {"date": d(2027, 3, 3), "title": "Golf — Daiatsugi Country Club",
             "detail": "A proper Japanese golf club experience, not just the convenient option: Daiatsugi CC "
                       "(Sakura Course), Kanagawa — Odakyu Line from Shinjuku to Hon-Atsugi (~1h), then a taxi/"
                       "shuttle (~1.5-1.75h door to door). Book via golf-in-japan.com. Green fee ~¥11,850-16,350 "
                       "(~€64-88) weekday, club rental available. Budget the WHOLE day: an 18-hole round in "
                       "Japan runs 5-6h including a mandatory sit-down lunch break after the front nine, plus "
                       "transit each way — leave ~6:30-7am, back ~7-8pm. (Kanagawa Country Club is a solid "
                       "backup in the same area/price band if Daiatsugi's booked out.)", "tag": "tourist"},
            {"date": d(2027, 3, 4), "title": "Ghibli Museum, Mitaka + Kichijoji & Shimokitazawa shopping",
             "detail": "Studio Ghibli Museum, then Inokashira Park — the Benzaiten Shrine on the pond's island, "
                       "paddleboats if the queue's short — and Kichijoji town itself, which has a genuinely good "
                       "vintage/select-shop scene of its own. Then one stop further on the Keio Inokashira Line "
                       "to Shimokitazawa — Tokyo's best thrift/vintage/indie-designer shopping district, dense "
                       "with small boutiques and secondhand stores, plus good cafes to break it up. BOOK GHIBLI "
                       "EARLY: tickets are timed-entry, released monthly (typically the 10th, ~1-3 months "
                       "ahead) and sell out fast — the one hard calendar reminder on this whole trip.", "tag": "city"},
            {"date": d(2027, 3, 5), "title": "Expo & bib pickup + Akihabara + Round1",
             "detail": "Collect race kit, carb-load begins. Then Akihabara for an anime/gaming/tech afternoon — "
                       "genuinely easy on the legs two days out since it's almost entirely indoor, multi-floor "
                       "browsing rather than distance walking: Yodobashi Akiba (cavernous electronics store), "
                       "the Mandarake Complex (8 floors of manga/anime/figures), Super Potato (retro gaming, "
                       "delightfully niche), an arcade for claw machines and rhythm games, and the Radio Kaikan "
                       "building for good measure. In the evening, a few Yamanote Line stops to Round1 Ikebukuro "
                       "(open 24h, 4 min walk from the station) for the full \"everything in one building\" "
                       "experience — bowling, arcade floors, karaoke, billiards, darts. TWO DAYS OUT FROM THE "
                       "RACE: stick to the arcade/karaoke/darts side and skip batting cages or bowling's actual "
                       "swinging motion — save that physical stuff for after the marathon, back at Round1 Osaka "
                       "if you want the full batting-cage experience. Keep the pace unhurried overall — browsing, "
                       "not a walking tour, and definitely not a workout.", "tag": "city"},
            {"date": d(2027, 3, 6), "title": "Shakeout, rest, Nakiryu ramen & sushi omakase carb-load",
             "detail": "Short shakeout + strides, lay out kit, early night. Lunch stop: Nakiryu in Sangenjaya — "
                       "the tantanmen shop that made history alongside Tsuta as one of Tokyo's first "
                       "Michelin-starred ramen restaurants (2017; Michelin has since folded the ramen category "
                       "out of its star listings, but the food and reputation haven't gone anywhere). Only 10 "
                       "seats, no reservations, so go early or expect a queue — genuinely low-impact the day "
                       "before the race since it's just standing, not walking. For the carb-load dinner: Kyubey "
                       "Ginza (Ginza Honten) — a long-established, genuinely foreigner-friendly omakase counter, "
                       "not an intimidating impossible-to-book legend like Jiro. Nigiri-only omakase from "
                       "¥10,000, full set courses ¥15,000-30,000; 17 seats means a reservation is sensible but "
                       "walk-ins can work at lunch if dinner's booked out. Rice-forward and light on heavy fats "
                       "makes this a genuinely sensible night-before meal, not just an indulgence — good protein "
                       "and carbs without the bloat of a big pasta blowout.", "tag": "rest"},
        ]},
        {"name": "Race day", "blurb": "", "days": [
            {"date": d(2027, 3, 7), "title": "🏁 TOKYO MARATHON",
             "detail": "Race day. Refuel, shower and rest up for a few hours first, then Shinjuku's Golden Gai "
                       "and Omoide Yokocho for the real celebration once the legs have had a chance to settle — "
                       "one of Tokyo's best nightlife pockets, and there's no better excuse for a proper night "
                       "out than just finishing a marathon. Gentle, seated drinking rather than a bar-hopping "
                       "crawl — cobblestone alleys and sore quads don't mix a few hours post-race.",
             "tag": "race"},
        ]},
        {"name": "Nakasendo Trail — Magome to Tsumago", "blurb": "The old Edo-period highway between Tokyo and "
                                                                   "Kyoto — back to two days (the rest-day "
                                                                   "experiment was nice but the day was needed "
                                                                   "elsewhere). A night "
                                                                   "in a preserved post town and a forest walk "
                                                                   "between two of Japan's best-kept historic "
                                                                   "villages.", "days": [
            {"date": d(2027, 3, 8), "title": "Tokyo → Magome",
             "detail": "The day after the race, genuinely easy on purpose: shinkansen to Nagoya, limited "
                       "express to Nakatsugawa, bus to Magome. A gentle look around the post town in the late "
                       "afternoon if legs allow, overnight in a traditional minshuku. Recovery-mode legs, no "
                       "rush — this slot used to be a full Tokyo sightseeing day (Shibuya, Harajuku, "
                       "go-karting), but with those moved earlier in the week to 1 March, the day after the "
                       "race is now free to just be a quiet travel day.", "tag": "travel"},
            {"date": d(2027, 3, 9), "title": "Walk to Tsumago, on to Kyoto",
             "detail": "The Magome-Tsumago walk: ~7.8 km, ~2.5-3 h through forest, waterfalls and Edo-period "
                       "checkpoints — genuinely one of Japan's best short walks, and legs have had 2 days to "
                       "recover since the race. Then bus/train to Nagiso, "
                       "limited express to Nagoya, shinkansen on to Kyoto by evening.", "tag": "city"},
        ]},
        {"name": "Kyoto & Nara", "blurb": "Four days now (the Arima Onsen day has been dropped, and the "
                                           "Ichijoji day now doubles as the transfer to Osaka instead) — "
                                           "temples, a sake brewery, Nara's Omizutori fire ritual if timing "
                                           "allows (1-14 Mar), a proper whisky day, and Musashi history, with "
                                           "the sightseeing condensed by pairing sights that sit right next to "
                                           "each other.", "days": [
            {"date": d(2027, 3, 10), "title": "Fushimi Inari & Fushimi sake brewery",
             "detail": "Fushimi Inari's torii-gate trail in the morning, then straight into Fushimi's historic "
                       "sake-brewing district (40+ breweries, famously soft water) right next door: Gekkeikan "
                       "Okura Sake Museum for the history + tasting, Kizakura Kappa Country as a second stop, "
                       "and a walk along the willow-lined Fushimi canal past the old sake warehouses. One "
                       "compact South Kyoto day instead of two, since the shrine and the sake district are "
                       "genuinely a short walk apart.", "tag": "city"},
            {"date": d(2027, 3, 11), "title": "Yamazaki Distillery whisky tour",
             "detail": "Suntory Yamazaki — Japan's oldest whisky distillery (1923) and the birthplace of "
                       "Japanese whisky, sitting almost exactly on the Kyoto/Osaka border. JR Yamazaki Station "
                       "is ~15 min from Kyoto Station on the JR Kyoto Line. A proper day trip out "
                       "and back to Kyoto rather than doubling as the transfer to Osaka — no bags to haul, no "
                       "trains to catch, just the tour and however long you want in the Whisky Library after. "
                       "Guided tours (English slots available) need advance online booking through Suntory's "
                       "site — the release window opens a few months out and English/premium slots sell out "
                       "fast, so treat this as another hard pre-booking deadline alongside the Ghibli Museum, "
                       "sumo tickets, and the go-karting IDP. Standard tour + tasting course ≈¥3,000-6,000 "
                       "depending on which whiskies are poured; the Whisky Library tasting counter and shop "
                       "(single-cask and distillery-exclusive bottlings) are open to walk-ins without a tour "
                       "reservation if the tour itself is sold out. Back to Kyoto for the night.", "tag": "tourist"},
            {"date": d(2027, 3, 12), "title": "Nara day-trip — Omizutori",
             "detail": "Todai-ji + the Omizutori fire ritual (torches on the temple veranda each evening, "
                       "runs 1-14 Mar — check that year's exact times).", "tag": "city"},
            {"date": d(2027, 3, 13), "title": "Gion, Kiyomizu-dera & Ichijoji Sagarimatsu, on to Osaka",
             "detail": "Morning/early afternoon in Higashiyama: Gion's old streets, Kiyomizu-dera. Then across "
                       "to Ichijoji in Sakyo-ku for Ichijoji Sagarimatsu — the pine and stone monument marking "
                       "the site of Musashi Miyamoto's most famous duel, alone against ~70 swordsmen of the "
                       "Yoshioka School (1604), the story that made his legend before Ganryujima. The current "
                       "pine is a later-generation descendant; the little Hachidai Shrine right next to it is "
                       "where Musashi is said to have paused before the fight. Quiet and non-touristy — if "
                       "there's time/energy left, the rest of the Ichijoji neighbourhood is worth it too: "
                       "Shisen-do (Ishikawa Jozan's Edo-period hermitage), Enko-ji (bamboo grove + hilltop view) "
                       "and Manshu-in, all a short walk apart. Ichijoji is also Kyoto's unofficial ramen street, "
                       "so grab something there before heading out. This is now also the Kyoto->Osaka transfer "
                       "day (the Arima Onsen day has been dropped) — leave Kyoto in the evening once you're "
                       "done in Ichijoji, arriving Osaka late that night. Higashiyama and Sakyo-ku are both "
                       "well served by bus, and a taxi hop between them is cheap if the legs are done by "
                       "mid-afternoon.", "tag": "city"},
        ]},
        {"name": "Osaka", "blurb": "Three days — castle, sumo, baseball, boat racing and some of Japan's best "
                                    "nightlife, spread out one headline per day instead of stacked on the last "
                                    "one, which frees up that evening to head straight to Niseko.", "days": [
            {"date": d(2027, 3, 14), "title": "Osaka Castle, boat racing, Kobe beef & Dotonbori",
             "detail": "Osaka Castle in the afternoon. FOR A FLUTTER on the way: Boat Race Suminoe (kyotei) "
                       "runs near-daily, cash betting, English signage, no ID/account needed — 3 min walk from "
                       "Suminoekoen Station, an easy detour before or after the castle. Dinner: a proper A5 "
                       "Kobe beef teppanyaki course right in "
                       "Dotonbori — Kobe Beef Wanomiya Dotonbori is well-regarded and easy to book, courses from "
                       "¥7,500, counter seating so you watch it cooked in front of you; no need to trek out to "
                       "Kobe itself (~30 min by train if you'd rather do the pilgrimage properly, but the beef "
                       "in Osaka is the same grade). Then straight into Dotonbori's street-food crawl for "
                       "afters (takoyaki, okonomiyaki, kushikatsu) once the neon's on.", "tag": "city"},
            {"date": d(2027, 3, 15), "title": "Grand Sumo, Namba & Shinsekai by night + Round1 Stadium",
             "detail": "THE real headline: the Haru Basho (Osaka's Grand Sumo Tournament) runs 14-28 Mar 2027 "
                       "at EDION Arena Osaka (formerly Osaka Prefectural Gymnasium), right in the middle of "
                       "this Osaka stay — book tickets as soon as they go on sale (roughly a month or so out, "
                       "via the official Sumo Association site or a ticket reseller). Cheap balcony/arena seats "
                       "from ~¥3,600-8,000; ringside box seats are pricier and sell out first. Bouts run all "
                       "afternoon into the top-division matches around 6pm, which times out nicely into the "
                       "evening: Namba's bars, Shinsekai's retro streets and Tsutenkaku tower — Osaka's "
                       "nightlife is a genuine highlight, not an afterthought. Then Round1 Stadium Sennichimae, "
                       "right at the edge of Namba/Dotonbori (Kintetsu Nippombashi Sta., exit B20) — the real "
                       "\"everything in one multi-storey building\" experience: 11 floors of bowling, batting "
                       "cages, 5 floors of arcade games, karaoke, darts, ping-pong, ice skating and Spo-Cha "
                       "(basketball, archery, mechanical bull). Bowling + the arcade floors run 24h; a few "
                       "individual attractions (batting, karaoke) have narrower hours, worth a quick check at "
                       "the front desk. Flat-rate \"free time\" pass ~¥2,000-2,900 for 2-3h, or pay per activity "
                       "(bowling ~¥500-800/game, batting ~¥100/set). English signage, easy for tourists.",
             "tag": "city"},
            {"date": d(2027, 3, 16), "title": "NPB baseball, then on to Niseko",
             "detail": "NPB preseason (\"open-sen\") games run into ~22 Mar — catch the Orix Buffaloes at Kyocera "
                       "Dome (in the city, most convenient) or the Hanshin Tigers at Koshien Stadium (short "
                       "Hanshin Line ride); Spring Koshien, the high-school tournament at the same stadium, "
                       "typically runs ~19-31 Mar too. Check the day's fixture/kick-off time — an early or "
                       "afternoon game leaves the evening free for the Niseko transfer below (this day used to "
                       "be its own separate travel day; spreading sumo/baseball/boat racing across all three "
                       "Osaka days instead of stacking them on this one frees up the evening for it instead). "
                       "Also worth checking closer to the time: Hanshin (Nishinomiya) or Kyoto Racecourse — JRA "
                       "horse racing alternates between the two most Sat/Sundays in season, though these "
                       "particular Osaka days fall midweek, so a meeting isn't guaranteed. THE TRANSFER: fly "
                       "Kansai (KIX) → New Chitose (~2.5h), then intercity bus to Niseko (~2.5-3h via Rusutsu) "
                       "— ~6.5-7.5h door to door, so an evening departure means a late arrival (past midnight is "
                       "realistic) — check in and go straight to bed, first day on the mountain starts fresh "
                       "the next morning. Shinkansen isn't competitive on this route; flying is unambiguously "
                       "the better option.", "tag": "travel"},
        ]},
        {"name": "Niseko — snowboarding", "blurb": "A few days on the mountain.", "days": [
            {"date": d(2027, 3, 17), "title": "Snowboarding, drinks & dinner in Niseko town",
             "detail": "Full day on the mountain. In the evening: drinks and dinner in Niseko town — plenty of "
                       "good izakayas, ramen and international spots catering to the ski crowd. (This was "
                       "originally meant to be arrival-night plans, but with the Niseko transfer now folded "
                       "into the last Osaka evening and landing well past midnight, there's no realistic window "
                       "for a proper night out on arrival — moved to this first full evening instead, once "
                       "everyone's actually awake and the legs have had a day on the mountain to loosen up.)",
             "tag": "snow"},
            {"date": d(2027, 3, 18), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 19), "title": "Snowboarding", "detail": "Last day riding.", "tag": "snow"},
        ]},
        {"name": "Sapporo", "blurb": "Just the one night now (was two) — Clock Tower by day, Susukino by night, "
                                      "then off after lunch. No racing here anyway: Sapporo Racecourse is "
                                      "summer-only (roughly late Jul-early Sep) and closed in March.", "days": [
            {"date": d(2027, 3, 20), "title": "Niseko → Sapporo, Susukino by night",
             "detail": "Transfer to Sapporo. Clock Tower, Odori Park, Nijo Market by day, then straight into "
                       "Susukino by night — ramen alley, izakayas, bars, Hokkaido's nightlife capital. Depart "
                       "the next afternoon, so no need to spread this over two full days: sightsee, eat, drink, "
                       "sleep it off in the morning. (No gambling detour worth it near here: Obihiro's unique "
                       "Banei Keiba — draft horses pulling sleds, only venue of its kind in the world — is "
                       "~2h15-2h45 each way by JR, a full day round trip. A genuine curiosity if it's a "
                       "bucket-list item, but not worth it for a one-night stop.)", "tag": "city"},
        ]},
        {"name": "Miyazaki", "blurb": "Two days now (was three) — Miyazaki has no useful Hokkaido link, but "
                                       "good direct flights to both Osaka (~1h) and Naha (~1h37m), so it's still "
                                       "the lowest-backtrack place in the whole route to fit it in.", "days": [
            {"date": d(2027, 3, 21), "title": "Sapporo → Miyazaki, night out with friends",
             "detail": "Depart Sapporo in the afternoon, connecting via Osaka (Itami) or Haneda — a long travel "
                       "day, arriving Miyazaki in the evening. NIGHT OUT: catching up with our Japanese friends "
                       "there — let them pick the spot, they'll know better than any guidebook. Worth keeping "
                       "the golf/Aoshima day after a little flexible on start time if it runs late.",
             "tag": "city"},
            {"date": d(2027, 3, 22), "title": "Golf — Phoenix Country Club, Aoshima Shrine & on to Naha",
             "detail": "THE nice round: home of the Dunlop Phoenix Tournament (JGTO), 27 holes along the "
                       "Hitotsuba pine coast, ranked among Japan's top courses. Members-club in name but "
                       "visitors are genuinely welcome — book via GDO/Rakuten GORA/Jalan golf, or ask the "
                       "Sheraton Grande Ocean Resort/Seagaia concierge next door. Green fee ≈¥31,000-58,000 "
                       "(≈€190-350) depending on day/season; caddie is compulsory (adds to cost), jacket needed "
                       "in the clubhouse outside summer. ~20 min from JR Miyazaki Station/the airport. Book an "
                       "early tee time (7-8am) — 18 holes with the compulsory caddie pace + clubhouse lunch "
                       "break runs 5-6h, so an early start gets you off the course by early-mid afternoon with "
                       "just enough left for Aoshima Shrine and the \"Devil's Washboard\" (Oni no Sentakuita) "
                       "tide-carved rock formations, an easy couple of hours nearby, before flying on to Naha in "
                       "the evening. A full day, but a doable one. (Takachiho Gorge is ~2.5h further with no "
                       "train access — skipped to keep this a single efficient stop; would need its own "
                       "overnight to do properly.)", "tag": "tourist"},
        ]},
        {"name": "Okinawa — Naha & Kerama", "blurb": "Trimmed down and spread out rather than 12 days in one "
                                                       "block. March suits sightseeing/snorkelling more than "
                                                       "full beach season (water ~22°C). 4th day added for a "
                                                       "good-value round of golf.", "days": [
            {"date": d(2027, 3, 23), "title": "Naha — a proper night out",
             "detail": "Shuri Castle by day. By night: Kokusai-dori's main strip, or for something more local, "
                       "Sakaemachi Market (15 min walk / one monorail stop to Asato) — tiny hole-in-the-wall "
                       "izakayas threaded between market stalls, awamori and ¥300 yakitori, comes alive after "
                       "6pm, mostly no English menus. The better night out of the two.", "tag": "city"},
            {"date": d(2027, 3, 24), "title": "Golf — Okinawa Country Club",
             "detail": "The good-value round: ~15-20 min taxi from Naha (Nishihara). Green fee ≈¥12,000-18,000 "
                       "(≈€75-110, official-site discounts knock off ¥500-1,000). Club rental from ¥5,500, "
                       "shoes ¥1,100 — no need to bring clubs. No handicap certificate required; that's an old "
                       "private-club norm, not a real barrier for visitor/resort play in Japan anymore.",
             "tag": "tourist"},
            {"date": d(2027, 3, 25), "title": "Churaumi Aquarium day-trip",
             "detail": "North-island day trip (rental car preferred): Churaumi Aquarium, Ocean Expo Park, "
                       "Bise Fukugi Tree Road.", "tag": "tourist"},
            {"date": d(2027, 3, 26), "title": "Kerama Islands day-trip",
             "detail": "Ferry to Zamami/Aka (50-70 min). Snorkelling at Furuzamami Beach — March is within "
                       "Kerama whale-watching season.", "tag": "tourist"},
        ]},
        {"name": "Travel home", "blurb": "", "days": [
            {"date": d(2027, 3, 27), "title": "Fly home", "detail": "Depart Japan from Naha.", "tag": "travel"},
        ]},
    ]
    ndays = sum(len(l["days"]) for l in legs)
    return {"meta": {"title": "Japan Trip 2027", "start": d(2027, 2, 27), "end": d(2027, 3, 27),
                     "days": ndays,
                     "note": "Tokyo (race week: Asakusa by day + Shibuya/Harajuku/teamLab/go-karting all "
                             "stacked onto the Monday — 6 days clear of the race, no need to hold back — snow "
                             "monkeys day trip, golf at Daiatsugi CC, Ghibli Museum + Kichijoji/Shimokitazawa "
                             "shopping, Akihabara + Round1 Ikebukuro, Nakiryu ramen the day before the race) -> "
                             "RACE -> Golden Gai that evening (a proper celebration fits post-race better than "
                             "a pre-race outing) -> 2 days on the Nakasendo Trail (Tokyo -> Magome, then the "
                             "Tsumago walk on to Kyoto) -> 4 days Kyoto/Nara (Fushimi Inari + sake brewery, a "
                             "Yamazaki whisky day trip, Nara/Omizutori, then Gion/Kiyomizu-dera/Ichijoji "
                             "Sagarimatsu doubling as the transfer to Osaka — leave that evening, arrive Osaka "
                             "late) -> 3 days Osaka (Haru Basho Grand Sumo Tournament, NPB baseball and Boat "
                             "Race Suminoe spread one per day rather than stacked, freeing the last evening for "
                             "a direct transfer to Niseko instead of a dedicated travel day; Kobe beef "
                             "teppanyaki + Round1 Stadium Sennichimae folded into the other two days) -> Niseko "
                             "(arriving late, drinks/dinner in Niseko town moved to the first full evening "
                             "instead of arrival night) -> Sapporo (1 night — arrive, sightsee, one night out "
                             "in Susukino, depart the next afternoon) -> Miyazaki (2 days — golf at Phoenix "
                             "Country Club shares a day with Aoshima Shrine, timed around an early tee slot; "
                             "night out with friends on arrival) -> Okinawa (4 nights, incl. golf at Okinawa "
                             "Country Club) -> home direct from Naha (Ishigaki dropped from the route "
                             "entirely). Sendai/Matsushima dropped throughout in favour of the extra Kyoto/"
                             "Osaka time. Three proper food experiences folded into existing days rather than "
                             "given their own: sushi omakase at Kyubey Ginza the night before the race, "
                             "Michelin-pedigree tantanmen at Nakiryu for lunch that same day, and Kobe beef "
                             "teppanyaki in Dotonbori. 29 days total — 4 shorter than the original 33, even "
                             "after everything added along the way (peaked at 37 mid-trip before this round of "
                             "trims: Nakasendo back to 2 days, Kyoto/Nara to 4 with Arima Onsen dropped, and "
                             "the old \"To Niseko\" travel day folded into Osaka's last evening). Cherry "
                             "blossoms are still a coin-flip: current estimate has peak bloom ~28 Mar-5 Apr, "
                             "and this trip now ends 27 Mar — a little ahead of that window rather than during "
                             "it; reconfirm closer to the time. Ghibli Museum tickets (4 Mar) and the Yamazaki "
                             "Distillery tour (11 Mar) both need booking ~1-3 months ahead, sumo tickets go on "
                             "sale roughly a month out (grab them the moment they do — Haru Basho is popular), "
                             "and the go-karting needs an International Driving Permit sorted before departure "
                             "— the four hard deadlines here."},
            "legs": legs, "budget": budget()}


def budget():
    return {
        "intro": "Per person, 2 people sharing rooms, departing Málaga. FX rate used: 1 EUR ≈ ¥185.5 "
                 "(current). Costed for the full 29-day route (Ishigaki dropped from the route entirely — "
                 "Okinawa now flies straight home from Naha — Sapporo trimmed to 1 night, Miyazaki to 2 days, "
                 "Nakasendo back to 2 days, Kyoto/Nara to 4 days with Arima Onsen dropped and Ichijoji doubling "
                 "as the Osaka transfer, and the old \"To Niseko\" travel day folded into Osaka's last evening "
                 "— Miyazaki + snow monkeys + the extra Kyoto/Osaka "
                 "days, incl. the Yamazaki whisky tour and Haru "
                 "Basho sumo tickets + three "
                 "golf rounds: "
                 "Daiatsugi in Tokyo, Phoenix in Miyazaki, Okinawa CC in Naha) — includes the "
                 "Sapporo->Miyazaki->Naha flight chain, the Tokyo->Nagano->Yudanaka rail round "
                 "trip, the sake brewery/baseball tickets, and all three green fees. The Middle column is "
                 "anchored on live-researched current prices (flights, JR fares, hotel/lift-pass/green fee "
                 "rates); Bare minimum and Luxury are reasoned extrapolations using standard hostel/ryokan/"
                 "business-class ratios — worth re-checking closer to booking rather than treating as "
                 "independently sourced.",
        "tiers": {"headers": ["Tier", "What it gets you"], "rows": [
            ["Bare minimum", "Hostel dorms/capsules, conbini + casual meals, budget/no-frills flights, self-guided everything."],
            ["Middle", "Business hotels, casual-to-mid restaurants, standard economy flights — the itinerary as planned."],
            ["Luxury", "5★ hotels/luxury ryokan (kaiseki dinners included), business class flights, private tours/guides, fine dining."],
        ]},
        "table": {"headers": ["Category", "Bare minimum", "Middle", "Luxury"], "rows": [
            ["Int'l flights (Málaga↔Naha, open-jaw)", "€700", "€975", "€3,900"],
            ["Domestic rail (incl. Nagano/snow monkeys, Kyoto→Osaka)", "€165", "€240", "€430"],
            ["Domestic flights (incl. Sapporo→Miyazaki→Naha chain)", "€235", "€330", "€640"],
            ["Accommodation (28 nights)", "€675", "€1,045", "€6,770"],
            ["Niseko lift passes (3 days)", "€200", "€200", "€200"],
            ["Food / local transport / incidentals (29 days)", "€1,550", "€2,090", "€5,800"],
            ["Golf (Daiatsugi + Phoenix CC + Okinawa CC, incl. caddie/rental)", "€330", "€400", "€560"],
            ["Other activities & tours (sake brewery, baseball/boat racing, Aoshima, go-karting, Akihabara arcades, Round1 x2, Ichijoji-area temple entries)", "€180", "€235", "€1,100"],
            ["Yamazaki Distillery whisky tour", "€10", "€25", "€110"],
            ["Haru Basho sumo tournament tickets", "€19", "€32", "€85"],
            ["Food experiences (Kyubey sushi omakase, Nakiryu ramen, Kobe beef teppanyaki)", "€100", "€155", "€310"],
        ]},
        "durations": {"headers": ["Duration", "Bare minimum", "Middle", "Luxury"], "rows": [
            ["Full itinerary (29 days, 27 Feb-27 Mar)", "≈€4,150", "≈€5,730", "≈€19,900"],
            ["3-week (~22 days)*", "≈€3,150", "≈€3,900", "≈€14,400"],
        ]},
        "notes": [
            "*3-week = drop Miyazaki (and its Phoenix CC round) and the Tokyo golf day entirely, and trim Tokyo "
            "(7→6 nights, keep the snow monkeys, drop nothing else), Naha (4→2, "
            "keeping the Okinawa CC round since it's cheap and easy) — same core route otherwise, including the "
            "Ichijoji and whisky days, tighter stays. The cheap add-ons (sake brewery, baseball, boat "
            "racing, whisky tour, sumo tickets) and all three food experiences stay in even at 3 "
            "weeks since none of them cost much or need a dedicated day.",
            "The swing between tiers is almost entirely flights and accommodation — food and activities "
            "barely move the needle by comparison.",
            "Golf is three fixed-price rounds, not really tier-scalable — Daiatsugi Country Club (Kanagawa, the "
            "\"proper club\" Tokyo option: ¥11,850-16,350/≈€64-88, ~1.5-1.75h out via Odakyu Line), Phoenix "
            "Country Club (Miyazaki, the splurge round: ¥31,000-58,000/≈€190-350, compulsory caddie), and "
            "Okinawa Country Club (Naha, the good-value round: ¥12,000-18,000/≈€75-110, club rental from "
            "¥5,500). The Luxury figure assumes premium-date booking + better caddie tips, not different courses.",
            "Niseko lift passes are essentially fixed regardless of tier (it's a set resort rate) — "
            "€200 pp for a 3-day pass (¥36,800 regular-season rate, official niseko.ne.jp pricing, "
            "checked 2026). Niseko/Hakuba lift prices have risen ~30-40% over the last ~2 years — mostly "
            "resorts pricing to heavy international demand (80-90% of Niseko visitors are foreign), not "
            "just yen weakness — so re-verify this closer to booking, it moves fast.",
            "The Miyazaki insertion is the single biggest domestic-flight cost driver here — three short hops "
            "(Sapporo→Osaka/Haneda→Miyazaki→Naha) instead of one direct Sendai→Naha routing from the earlier "
            "version. Worth knowing that's what you're paying for the detour.",
            "The luxury total is dominated by business-class flights (~4x economy) and 28 nights of "
            "5★/ryokan. \"Luxury lodging but economy flights\" comes out to roughly €7,930–9,200 pp — a "
            "more common real-world middle ground if the full luxury number is too steep.",
            "WHEN TO BOOK — international flights: aim for Sept-Nov 2026 (5-6 months out). Google/Hopper fare "
            "data favours this window for Asia long-haul specifically over generic 'book last minute' advice; "
            "don't wait past Dec 2026. Tokyo Marathon weekend (7 Mar, 20th anniversary, ~40,000 runners) pushes "
            "Tokyo-area hotel prices ~7-13% above the otherwise-low shoulder season, so book Tokyo lodging on "
            "the earlier side of that window too, not on general 'low season, no rush' logic.",
            "WHEN TO BOOK — domestic Japan flights: ANA/JAL open bookings 355 days out (~Feb-Mar 2026) and "
            "their cheapest fare tiers (e.g. ANA SUPER VALUE 75/55/45/28/21) are inventory-limited, not "
            "fixed-price — the cheap seats sell out first even with the window still open. Book as soon as it "
            "opens if possible, and no later than ~75 days before each flight (~mid-Dec 2026) for the cheapest "
            "bucket. The Sapporo leg carries extra sellout risk from ski-season demand. Peach/Jetstar are pure "
            "dynamic pricing with no advance-purchase discount — just book as soon as they open seat sales for "
            "the season (~late Jan 2026).",
            "The 'book on a Tuesday' day-of-week folklore is debunked by the largest datasets (Google: "
            "1.3-1.9% difference; CheapAir: <$1 across 1B+ fares) — don't plan around it, the booking-window "
            "timing above matters far more.",
        ],
    }
