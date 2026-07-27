"""Japan trip itinerary — Tokyo (race week incl. Ghibli Museum, snow monkeys & Golden
Gai), Shibuya/Harajuku the day after the race, the Nakasendo Trail (Magome-Tsumago)
between Tokyo and Kyoto, Kyoto/Nara (incl. a Fushimi sake brewery, Ichijoji Sagarimatsu &
an Arima Onsen day), Osaka (incl. the Haru Basho sumo tournament + NPB preseason
baseball), Niseko, Sapporo, Miyazaki (Kyushu) on the way south, then Okinawa.
build() -> trip dict.

Route (27 Feb - 31 Mar 2027, 33 days): Tokyo race week (Ghibli Museum, Golden Gai on the
Monday — 6 days clear of the race so no need to hold back, snow monkeys day trip to
Jigokudani/Nagano) -> RACE -> Shibuya/Harajuku the day after (moved here on request) ->
a night on the Nakasendo Trail -> 4 days Kyoto/Nara (incl. a Fushimi sake brewery, the
Ichijoji Sagarimatsu/Musashi duel site + Kyoto's quiet northeast, and an Arima Onsen day
that doubles as the transfer to Osaka) -> 3 days Osaka (incl. the Haru Basho Grand Sumo
Tournament + NPB preseason baseball) -> Niseko -> Sapporo -> Miyazaki (1 night, inserted
here specifically
because it has good direct flights to/from Osaka AND Naha but nothing useful to Hokkaido,
so this is the lowest-backtrack slot) -> Okinawa (Naha/Kerama, incl. a proper night out)
-> home. Ishigaki dropped from the route entirely (on request) rather than trimmed, so
Okinawa now flies straight home from Naha instead of via a Naha<->Ishigaki hop. Sendai/
Matsushima dropped in favour of the extra Kyoto/Osaka day each; Kyoto/Nara grew by two
extra days for the Ichijoji and Arima Onsen additions, then condensed back to one net
extra day by pairing sights that sit next to each other (Fushimi Inari + the sake
brewery; Gion/Kiyomizu-dera + Ichijoji), pushing the END date from 2 Apr to 31 Mar overall
once Ishigaki's 3 days (2 there + 1 transfer) came back out."""
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
            {"date": d(2027, 3, 1), "title": "Asakusa & Senso-ji by day, Golden Gai by night",
             "detail": "Daytime: Senso-ji temple, Nakamise shopping street, Sumida river walk. Then Shinjuku's "
                       "Golden Gai and Omoide Yokocho for a proper night out — one of Tokyo's best nightlife "
                       "pockets. The night out is deliberately on the Monday: 6 days clear of the race instead "
                       "of 2, so there's no need to hold back.", "tag": "city"},
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
            {"date": d(2027, 3, 6), "title": "Shakeout & rest + sushi omakase carb-load",
             "detail": "Short shakeout + strides, lay out kit, early night. For the carb-load dinner: Kyubey "
                       "Ginza (Ginza Honten) — a long-established, genuinely foreigner-friendly omakase counter, "
                       "not an intimidating impossible-to-book legend like Jiro. Nigiri-only omakase from "
                       "¥10,000, full set courses ¥15,000-30,000; 17 seats means a reservation is sensible but "
                       "walk-ins can work at lunch if dinner's booked out. Rice-forward and light on heavy fats "
                       "makes this a genuinely sensible night-before meal, not just an indulgence — good protein "
                       "and carbs without the bloat of a big pasta blowout.", "tag": "rest"},
        ]},
        {"name": "Race day", "blurb": "", "days": [
            {"date": d(2027, 3, 7), "title": "🏁 TOKYO MARATHON",
             "detail": "Race day. Then eat, drink (in moderation) and celebrate.", "tag": "race"},
        ]},
        {"name": "Tokyo — after the race", "blurb": "One more Tokyo day before heading out — legs are trashed, "
                                                       "so keep it to easy walking, people-watching, and sitting "
                                                       "down to drive things.", "days": [
            {"date": d(2027, 3, 8), "title": "Shibuya, Harajuku, Michelin ramen & street go-karting",
             "detail": "Shibuya Crossing, Harajuku's Takeshita Street, teamLab (Planets or Borderless) if tickets "
                       "allow. Lunch detour: Nakiryu in Sangenjaya, one stop from Shibuya on the Tokyu Denentoshi "
                       "Line — the tantanmen shop that made history alongside Tsuta as one of Tokyo's first "
                       "Michelin-starred ramen restaurants (2017; Michelin has since folded the ramen category "
                       "out of its star listings, but the food and the reputation haven't gone anywhere). Only "
                       "10 seats, no reservations, so go early or expect a queue — fine on trashed legs since "
                       "it's just standing, not walking. Then real-life Mario Kart: public-road go-karting "
                       "through Tokyo in costume — the "
                       "original \"MariCAR\" brand was sued by Nintendo and rebranded (now mainly trading as "
                       "\"Street Kart\"; costumes are no longer Nintendo characters but the karting itself is "
                       "the same). SORT BEFORE YOU FLY: you need an International Driving Permit (1949 Geneva "
                       "Convention) arranged in your home country before departure — this can't be sorted in "
                       "Japan, same category of hard deadline as the Ghibli tickets. Low-impact seated activity, "
                       "fine the day after the race even with sore legs.", "tag": "city"},
        ]},
        {"name": "Nakasendo Trail — Magome to Tsumago", "blurb": "The old Edo-period highway between Tokyo and "
                                                                   "Kyoto — a night in a preserved post town and "
                                                                   "a forest walk between two of Japan's "
                                                                   "best-kept historic villages.", "days": [
            {"date": d(2027, 3, 9), "title": "Tokyo → Magome",
             "detail": "Shinkansen to Nagoya, limited express to Nakatsugawa, bus to Magome. Explore the post "
                       "town in the afternoon, overnight in a traditional minshuku. Recovery-mode legs, no rush.",
             "tag": "travel"},
            {"date": d(2027, 3, 10), "title": "Walk to Tsumago, on to Kyoto",
             "detail": "The Magome-Tsumago walk: ~7.8 km, ~2.5-3 h through forest, waterfalls and Edo-period "
                       "checkpoints — genuinely one of Japan's best short walks. Then bus/train to Nagiso, "
                       "limited express to Nagoya, shinkansen on to Kyoto by evening.", "tag": "city"},
        ]},
        {"name": "Kyoto & Nara", "blurb": "Four days now (was three, briefly five) — temples, a sake brewery, "
                                           "Nara's Omizutori fire ritual if timing allows (1-14 Mar), Musashi "
                                           "history, and a proper onsen day, condensed by pairing sights that "
                                           "sit right next to each other.", "days": [
            {"date": d(2027, 3, 11), "title": "Fushimi Inari & Fushimi sake brewery",
             "detail": "Fushimi Inari's torii-gate trail in the morning, then straight into Fushimi's historic "
                       "sake-brewing district (40+ breweries, famously soft water) right next door: Gekkeikan "
                       "Okura Sake Museum for the history + tasting, Kizakura Kappa Country as a second stop, "
                       "and a walk along the willow-lined Fushimi canal past the old sake warehouses. One "
                       "compact South Kyoto day instead of two, since the shrine and the sake district are "
                       "genuinely a short walk apart.", "tag": "city"},
            {"date": d(2027, 3, 12), "title": "Gion, Kiyomizu-dera & Ichijoji Sagarimatsu",
             "detail": "Morning/early afternoon in Higashiyama: Gion's old streets, Kiyomizu-dera. Then across "
                       "to Ichijoji in Sakyo-ku for Ichijoji Sagarimatsu — the pine and stone monument marking "
                       "the site of Musashi Miyamoto's most famous duel, alone against ~70 swordsmen of the "
                       "Yoshioka School (1604), the story that made his legend before Ganryujima. The current "
                       "pine is a later-generation descendant; the little Hachidai Shrine right next to it is "
                       "where Musashi is said to have paused before the fight. Quiet and non-touristy — if "
                       "there's time/energy left, the rest of the Ichijoji neighbourhood is worth it too: "
                       "Shisen-do (Ishikawa Jozan's Edo-period hermitage), Enko-ji (bamboo grove + hilltop view) "
                       "and Manshu-in, all a short walk apart. Ichijoji is also Kyoto's unofficial ramen street, "
                       "so it doubles as a good dinner stop to close out a full day. Busier than a dedicated "
                       "Ichijoji day would have been, but Higashiyama and Sakyo-ku are both well served by bus "
                       "and a taxi hop between them is cheap if the legs are done by mid-afternoon.", "tag": "city"},
            {"date": d(2027, 3, 13), "title": "Nara day-trip — Omizutori",
             "detail": "Todai-ji + the Omizutori fire ritual (torches on the temple veranda each evening, "
                       "runs 1-14 Mar — check that year's exact times).", "tag": "city"},
            {"date": d(2027, 3, 14), "title": "Arima Onsen, on to Osaka",
             "detail": "Swapped out the whisky distillery for this — nobody wants to be half-cut right before "
                       "hauling bags onto a train. Arima Onsen instead: one of Japan's oldest and most famous "
                       "hot spring towns, tucked in the hills above Kobe, en route to Osaka rather than a "
                       "detour. ~1h from Kyoto (Hankyu + Kobe Dentetsu lines, ~¥800-900) or a direct highway "
                       "bus with no transfers. Arima Grand Hotel does day-use bathing (kannai-riyouken) without "
                       "a reservation — ¥4,000 weekday/¥4,500 weekend, which includes a ¥2,000 facility "
                       "voucher — or pick any of the other ryokan offering day baths if it's booked. Try both "
                       "of Arima's two distinct spring types: kinsen (\"gold spring\", iron-rich, rust-coloured) "
                       "and ginsen (\"silver spring\", clear, radium/carbonate). Wander the old town's narrow "
                       "streets and Taiko-no-Yu footbath after soaking, then continue on to Osaka by train in "
                       "the afternoon/evening (~1h).", "tag": "tourist"},
        ]},
        {"name": "Osaka", "blurb": "Three days now instead of two — castle, baseball, and some of Japan's best "
                                    "nightlife.", "days": [
            {"date": d(2027, 3, 15), "title": "Osaka Castle, Kobe beef teppanyaki & Dotonbori",
             "detail": "Osaka Castle in the afternoon. Dinner: a proper A5 Kobe beef teppanyaki course right in "
                       "Dotonbori — Kobe Beef Wanomiya Dotonbori is well-regarded and easy to book, courses from "
                       "¥7,500, counter seating so you watch it cooked in front of you; no need to trek out to "
                       "Kobe itself (~30 min by train if you'd rather do the pilgrimage properly, but the beef "
                       "in Osaka is the same grade). Then straight into Dotonbori's street-food crawl for "
                       "afters (takoyaki, okonomiyaki, kushikatsu) once the neon's on.", "tag": "city"},
            {"date": d(2027, 3, 16), "title": "Namba & Shinsekai by night + Round1 Stadium",
             "detail": "Namba's bars, Shinsekai's retro streets and Tsutenkaku tower — Osaka's nightlife is a "
                       "genuine highlight, not an afterthought. Then Round1 Stadium Sennichimae, right at the "
                       "edge of Namba/Dotonbori (Kintetsu Nippombashi Sta., exit B20) — the real \"everything in "
                       "one multi-storey building\" experience: 11 floors of bowling, batting cages, 5 floors of "
                       "arcade games, karaoke, darts, ping-pong, ice skating and Spo-Cha (basketball, archery, "
                       "mechanical bull). Bowling + the arcade floors run 24h; a few individual attractions "
                       "(batting, karaoke) have narrower hours, worth a quick check at the front desk. Flat-rate "
                       "\"free time\" pass ~¥2,000-2,900 for 2-3h, or pay per activity (bowling ~¥500-800/game, "
                       "batting ~¥100/set). English signage, easy for tourists.", "tag": "city"},
            {"date": d(2027, 3, 17), "title": "Grand Sumo, NPB baseball & boat racing",
             "detail": "THE real headline: the Haru Basho (Osaka's Grand Sumo Tournament) runs 14-28 Mar 2027 "
                       "at EDION Arena Osaka (formerly Osaka Prefectural Gymnasium), right in the middle of "
                       "this Osaka stay — book tickets as soon as they go on sale (roughly a month or so out, "
                       "via the official Sumo Association site or a ticket reseller). Cheap balcony/arena seats "
                       "from ~¥3,600-8,000; ringside box seats are pricier and sell out first, but any seat gets "
                       "you the full day's under-card through the top-division bouts in the evening. NPB "
                       "preseason (\"open-sen\") games also run into ~22 Mar if baseball's more your thing — "
                       "Orix Buffaloes at Kyocera Dome (in the city) or Hanshin Tigers at Koshien Stadium (short "
                       "Hanshin Line ride); Spring Koshien, the high-school tournament at the same stadium, "
                       "typically runs ~19-31 Mar too. FOR A FLUTTER: Boat Race Suminoe (kyotei) runs "
                       "near-daily, cash betting, English signage, no ID/account needed — 3 min walk from "
                       "Suminoekoen Station. Also worth checking closer to the time: Hanshin (Nishinomiya) or "
                       "Kyoto Racecourse — JRA horse racing alternates between the two most Sat/Sundays in "
                       "season, though these particular Osaka days now fall midweek, so a meeting isn't "
                       "guaranteed — check the JRA calendar and shift a day or two if it matters to you.",
             "tag": "city"},
        ]},
        {"name": "To Niseko", "blurb": "A full travel day, not a quick hop — budget for it.", "days": [
            {"date": d(2027, 3, 18), "title": "Osaka → Niseko",
             "detail": "Fly Kansai (KIX) → New Chitose (~2.5h), then intercity bus to Niseko (~2.5-3h via "
                       "Rusutsu) — ~6.5-7.5h door to door. Shinkansen isn't competitive on this route; flying "
                       "is unambiguously the better option.", "tag": "travel"},
        ]},
        {"name": "Niseko — snowboarding", "blurb": "A few days on the mountain.", "days": [
            {"date": d(2027, 3, 19), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 20), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 21), "title": "Snowboarding", "detail": "Last day riding.", "tag": "snow"},
        ]},
        {"name": "Sapporo", "blurb": "Clock Tower by day, Susukino — one of Japan's biggest entertainment "
                                      "districts — by night. No racing here though: Sapporo Racecourse is "
                                      "summer-only (roughly late Jul-early Sep) and closed in March.", "days": [
            {"date": d(2027, 3, 22), "title": "Niseko → Sapporo",
             "detail": "Transfer to Sapporo. Clock Tower, Odori Park, Nijo Market.", "tag": "city"},
            {"date": d(2027, 3, 23), "title": "Susukino by night",
             "detail": "Ramen alley, izakayas, bars — Susukino is Hokkaido's nightlife capital. (No gambling "
                       "detour worth it near here: Obihiro's unique Banei Keiba — draft horses pulling sleds, "
                       "only venue of its kind in the world — is ~2h15-2h45 each way by JR, a full day round "
                       "trip. A genuine curiosity if it's a bucket-list item, but not worth it for a 2-day stop.)",
             "tag": "city"},
        ]},
        {"name": "Miyazaki", "blurb": "One night, inserted here on purpose: Miyazaki has no useful Hokkaido "
                                       "link, but good direct flights to both Osaka (~1h) and Naha (~1h37m) — "
                                       "this is the lowest-backtrack place in the whole route to fit it in.", "days": [
            {"date": d(2027, 3, 24), "title": "Sapporo → Miyazaki",
             "detail": "Connects via Osaka (Itami) or Haneda — a long travel day, arriving Miyazaki in the "
                       "evening.", "tag": "travel"},
            {"date": d(2027, 3, 25), "title": "Golf — Phoenix Country Club",
             "detail": "THE nice round: home of the Dunlop Phoenix Tournament (JGTO), 27 holes along the "
                       "Hitotsuba pine coast, ranked among Japan's top courses. Members-club in name but "
                       "visitors are genuinely welcome — book via GDO/Rakuten GORA/Jalan golf, or ask the "
                       "Sheraton Grande Ocean Resort/Seagaia concierge next door. Green fee ≈¥31,000-58,000 "
                       "(≈€190-350) depending on day/season; caddie is compulsory (adds to cost), jacket needed "
                       "in the clubhouse outside summer. ~20 min from JR Miyazaki Station/the airport. Given the "
                       "compulsory caddie pace + clubhouse time it eats most of a day — that's why Miyazaki got "
                       "a 3rd day rather than squeezing this in alongside Aoshima.", "tag": "tourist"},
            {"date": d(2027, 3, 26), "title": "Aoshima Shrine & on to Naha",
             "detail": "Aoshima Shrine and the \"Devil's Washboard\" (Oni no Sentakuita) tide-carved rock "
                       "formations, an easy couple of hours near the city. (Takachiho Gorge is ~2.5h further "
                       "with no train access — skipped to keep this a single efficient stop; would need its own "
                       "overnight to do properly.) Fly on to Naha in the afternoon/evening.", "tag": "tourist"},
        ]},
        {"name": "Okinawa — Naha & Kerama", "blurb": "Trimmed down and spread out rather than 12 days in one "
                                                       "block. March suits sightseeing/snorkelling more than "
                                                       "full beach season (water ~22°C). 4th day added for a "
                                                       "good-value round of golf.", "days": [
            {"date": d(2027, 3, 27), "title": "Naha — a proper night out",
             "detail": "Shuri Castle by day. By night: Kokusai-dori's main strip, or for something more local, "
                       "Sakaemachi Market (15 min walk / one monorail stop to Asato) — tiny hole-in-the-wall "
                       "izakayas threaded between market stalls, awamori and ¥300 yakitori, comes alive after "
                       "6pm, mostly no English menus. The better night out of the two.", "tag": "city"},
            {"date": d(2027, 3, 28), "title": "Golf — Okinawa Country Club",
             "detail": "The good-value round: ~15-20 min taxi from Naha (Nishihara). Green fee ≈¥12,000-18,000 "
                       "(≈€75-110, official-site discounts knock off ¥500-1,000). Club rental from ¥5,500, "
                       "shoes ¥1,100 — no need to bring clubs. No handicap certificate required; that's an old "
                       "private-club norm, not a real barrier for visitor/resort play in Japan anymore.",
             "tag": "tourist"},
            {"date": d(2027, 3, 29), "title": "Churaumi Aquarium day-trip",
             "detail": "North-island day trip (rental car preferred): Churaumi Aquarium, Ocean Expo Park, "
                       "Bise Fukugi Tree Road.", "tag": "tourist"},
            {"date": d(2027, 3, 30), "title": "Kerama Islands day-trip",
             "detail": "Ferry to Zamami/Aka (50-70 min). Snorkelling at Furuzamami Beach — March is within "
                       "Kerama whale-watching season.", "tag": "tourist"},
        ]},
        {"name": "Travel home", "blurb": "", "days": [
            {"date": d(2027, 3, 31), "title": "Fly home", "detail": "Depart Japan from Naha.", "tag": "travel"},
        ]},
    ]
    ndays = sum(len(l["days"]) for l in legs)
    return {"meta": {"title": "Japan Trip 2027", "start": d(2027, 2, 27), "end": d(2027, 3, 31),
                     "days": ndays,
                     "note": "Tokyo (race week: Asakusa by day + Golden Gai by night on the Monday, snow monkeys "
                             "day trip, golf at Daiatsugi CC, Ghibli Museum + Kichijoji/Shimokitazawa shopping, "
                             "Akihabara + Round1 Ikebukuro) -> RACE -> Shibuya/Harajuku + go-karting the day "
                             "after -> a night on the Nakasendo Trail (Magome-Tsumago) -> 4 days Kyoto/Nara "
                             "(incl. Fushimi sake brewery, Ichijoji Sagarimatsu & Kyoto's quiet northeast, "
                             "Arima Onsen) -> 3 days Osaka (incl. the Haru Basho Grand Sumo Tournament + NPB "
                             "baseball + Boat Race Suminoe + Round1 Stadium Sennichimae) -> Niseko -> "
                             "Sapporo -> Miyazaki (3 nights, incl. golf at Phoenix Country Club) -> Okinawa "
                             "(4 nights, incl. golf at Okinawa Country Club) -> home direct from Naha. Ishigaki "
                             "dropped from the route entirely (on request), so there's no Naha<->Ishigaki hop "
                             "at the end any more. Sendai/Matsushima dropped in favour of the extra Kyoto/Osaka "
                             "day each. Miyazaki "
                             "and Naha each grew by a day to fit a round of golf properly (compulsory-caddie "
                             "rounds eat most of a day); Tokyo's golf slot needed no extra day at all — moving "
                             "Asakusa onto the same day as Golden Gai freed up the Wednesday for it, so the "
                             "week is back to its original 7 days. Kyoto/Nara grew from 3 to 5 days for the "
                             "Ichijoji/Musashi history day and a proper onsen day (Arima, swapped in for a "
                             "whisky distillery tour — nicer not to be tipsy right before hauling bags onto a "
                             "train), then condensed back "
                             "to 4: Fushimi Inari now shares a day with the Fushimi sake brewery next door, and "
                             "Gion/Kiyomizu-dera now shares a day with Ichijoji (both fit better with each other "
                             "than the original split did, and the onsen day still doubles as the Kyoto->Osaka "
                             "travel day, so it's not fully 'extra'). Osaka's dates now line up with the Haru "
                             "Basho — Osaka's Grand Sumo Tournament, running 14-28 Mar 2027 at EDION Arena, "
                             "right through the whole Osaka stay. Three proper food "
                             "experiences folded into existing days rather than given their own: sushi omakase "
                             "at Kyubey Ginza the night before the race, Michelin-pedigree tantanmen at Nakiryu "
                             "the day after, and Kobe beef teppanyaki in Dotonbori on the first Osaka night. 33 "
                             "days total — net unchanged from the original 33 once Ishigaki's 3 days (2 there + "
                             "1 transfer) came back out; the Kyoto/Nara growth and the Ishigaki removal happen "
                             "to cancel out almost exactly. Cherry blossoms are still a coin-flip: current "
                             "estimate has peak bloom ~28 "
                             "Mar-5 Apr — this trip now ends right at the start of that window rather than "
                             "comfortably inside it, so it's more likely you land home just before peak bloom "
                             "than during it; reconfirm closer to the time. Ghibli Museum tickets (4 Mar) need "
                             "booking ~1-3 months ahead, sumo "
                             "tickets go on sale roughly a month out (grab them the moment they do — Haru Basho "
                             "is popular), and the go-karting needs an "
                             "International Driving Permit sorted before departure — the three hard deadlines "
                             "here."},
            "legs": legs, "budget": budget()}


def budget():
    return {
        "intro": "Per person, 2 people sharing rooms, departing Málaga. FX rate used: 1 EUR ≈ ¥185.5 "
                 "(current). Costed for the full 33-day route (Ishigaki dropped from the route entirely — "
                 "Okinawa now flies straight home from Naha — Miyazaki + snow monkeys + the extra Kyoto/Osaka "
                 "days, incl. the Ichijoji/Musashi day, the Arima Onsen day and Haru Basho sumo tickets + three "
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
            ["Accommodation (32 nights)", "€770", "€1,200", "€7,740"],
            ["Niseko lift passes (3 days)", "€200", "€200", "€200"],
            ["Food / local transport / incidentals (33 days)", "€1,770", "€2,390", "€6,600"],
            ["Golf (Daiatsugi + Phoenix CC + Okinawa CC, incl. caddie/rental)", "€330", "€400", "€560"],
            ["Other activities & tours (sake brewery, baseball/boat racing, Aoshima, go-karting, Akihabara arcades, Round1 x2, Ichijoji-area temple entries)", "€180", "€235", "€1,100"],
            ["Arima Onsen day-use bathing", "€10", "€22", "€55"],
            ["Haru Basho sumo tournament tickets", "€19", "€32", "€85"],
            ["Food experiences (Kyubey sushi omakase, Nakiryu ramen, Kobe beef teppanyaki)", "€100", "€155", "€310"],
        ]},
        "durations": {"headers": ["Duration", "Bare minimum", "Middle", "Luxury"], "rows": [
            ["Full itinerary (33 days, 27 Feb-31 Mar)", "≈€4,480", "≈€6,180", "≈€21,600"],
            ["3-week (~24 days)*", "≈€3,400", "≈€4,220", "≈€15,600"],
        ]},
        "notes": [
            "*3-week = drop Miyazaki (and its Phoenix CC round) and the Tokyo golf day entirely, and trim Tokyo "
            "(7→6 nights, keep the snow monkeys, drop nothing else), Naha (4→2, "
            "keeping the Okinawa CC round since it's cheap and easy) — same core route otherwise, including the "
            "Ichijoji and onsen days, tighter stays. The cheap add-ons (sake brewery, baseball, boat racing, "
            "onsen day, sumo tickets) and all three food experiences stay in even at 3 weeks since none of them "
            "cost much or need a dedicated day.",
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
            "The luxury total is dominated by business-class flights (~4x economy) and 32 nights of "
            "5★/ryokan. \"Luxury lodging but economy flights\" comes out to roughly €9,100–10,500 pp — a "
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
