"""Japan trip itinerary — Osaka, Kyoto/Nara, Tokyo Marathon, Sendai/Matsushima,
Niseko, Sapporo, Okinawa & the Yaeyama Islands. build() -> trip dict.
Extended to a 4th week (27 Feb - 28 Mar 2027) with Okinawa/Ishigaki added at
the end. The 24-27 Mar block includes a deliberate weather/ferry contingency
day (island-hopping itineraries need one). NOTE: the Osaka Grand Sumo
tournament (~13-28 Mar 2027) overlaps this trip but not the Osaka leg itself
(we're in Kansai 1-5 Mar) — flagged as a trade-off, not missed by oversight."""
from datetime import date


def d(y, m, dd):
    return date(y, m, dd).isoformat()


def build():
    legs = [
        {"name": "Travel out", "blurb": "Depart & fly to Japan.", "days": [
            {"date": d(2027, 2, 27), "title": "Depart for Japan",
             "detail": "Long-haul out — arrive the next day depending on route (via Osaka/Kansai or direct to Tokyo).",
             "tag": "travel"},
        ]},
        {"name": "Kyoto & Nara", "blurb": "Temples, food, and — if timing lines up — Nara's Omizutori fire ritual (1-14 Mar).", "days": [
            {"date": d(2027, 2, 28), "title": "Arrive & settle",
             "detail": "Land, transfer to Kyoto, check in. Easy walking only — race is 7 days out.", "tag": "travel"},
            {"date": d(2027, 3, 1), "title": "Kyoto sightseeing",
             "detail": "Fushimi Inari, Gion, Kiyomizu-dera.", "tag": "city"},
            {"date": d(2027, 3, 2), "title": "Kyoto sightseeing",
             "detail": "Arashiyama bamboo grove, Kinkaku-ji, Nishiki Market.", "tag": "city"},
            {"date": d(2027, 3, 3), "title": "Nara day-trip — Omizutori",
             "detail": "Todai-ji + the Omizutori fire ritual (torches on the temple veranda each evening, "
                       "runs 1-14 Mar — check that year's exact times). A genuinely rare thing to catch.",
             "tag": "city"},
        ]},
        {"name": "Osaka", "blurb": "One dense day — castle by daylight, Dotonbori by night.", "days": [
            {"date": d(2027, 3, 4), "title": "Kyoto → Osaka",
             "detail": "Osaka Castle in the afternoon, then Dotonbori for a proper street-food crawl "
                       "(takoyaki, okonomiyaki, kushikatsu) once the neon's on.", "tag": "city"},
        ]},
        {"name": "To Tokyo — race week", "blurb": "Expo, carb-load, keep it low-key.", "days": [
            {"date": d(2027, 3, 5), "title": "Osaka → Tokyo",
             "detail": "Shinkansen to Tokyo, check in, expo & bib pickup, light sightseeing (Shibuya/Harajuku), "
                       "carb-load begins.", "tag": "travel"},
            {"date": d(2027, 3, 6), "title": "Shakeout & rest",
             "detail": "Short shakeout + strides, full carb-load, lay out race kit, early night.", "tag": "rest"},
        ]},
        {"name": "Race day", "blurb": "", "days": [
            {"date": d(2027, 3, 7), "title": "🏁 TOKYO MARATHON",
             "detail": "Race day. Then eat, drink (in moderation) and celebrate.", "tag": "race"},
        ]},
        {"name": "Tokyo recovery", "blurb": "One full day off your feet before heading north.", "days": [
            {"date": d(2027, 3, 8), "title": "Recovery day",
             "detail": "Legs up, short walk only, onsen/massage if you can find one, eat properly.", "tag": "rest"},
        ]},
        {"name": "Sendai & Matsushima", "blurb": "Direct on the Tohoku Shinkansen north — no backtracking, "
                                                   "and Matsushima Bay is one of Japan's official Three Views.", "days": [
            {"date": d(2027, 3, 9), "title": "Tokyo → Sendai",
             "detail": "~1.5h shinkansen. Afternoon: Zuihoden (Date Masamune's mausoleum), Aoba Castle ruins.",
             "tag": "travel"},
            {"date": d(2027, 3, 10), "title": "Matsushima day-trip",
             "detail": "~40 min local train from Sendai. Boat cruise through the pine-covered islets — "
                       "one of the Three Views of Japan, and it earns the title.", "tag": "city"},
        ]},
        {"name": "To Niseko", "blurb": "The long travel day — Tohoku up into Hokkaido.", "days": [
            {"date": d(2027, 3, 11), "title": "Sendai → Niseko",
             "detail": "Shinkansen via Shin-Aomori and the Hokkaido Shinkansen to Shin-Hakodate-Hokuto, then "
                       "onward to Niseko. A full day of trains — worth it to avoid backtracking through Tokyo.",
             "tag": "travel"},
        ]},
        {"name": "Niseko — snowboarding", "blurb": "A few days on the mountain.", "days": [
            {"date": d(2027, 3, 12), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 13), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 14), "title": "Snowboarding", "detail": "Last day riding.", "tag": "snow"},
        ]},
        {"name": "Sapporo", "blurb": "A day in the city before flying south to the warmth.", "days": [
            {"date": d(2027, 3, 15), "title": "Niseko → Sapporo",
             "detail": "Transfer to Sapporo. Clock Tower, Odori Park, Nijo Market, ramen alley.", "tag": "city"},
        ]},
        {"name": "Naha & Kerama Islands", "blurb": "Okinawa, as requested — warm finish to the trip. March is "
                                                     "good for sightseeing/snorkeling, not full beach season "
                                                     "(water ~22°C, official beach season starts late Mar).", "days": [
            {"date": d(2027, 3, 16), "title": "Sapporo → Naha",
             "detail": "Direct flight via New Chitose (~3h25-45m, roughly 1x/day — book early). "
                       "Warm evening, ease in.", "tag": "travel"},
            {"date": d(2027, 3, 17), "title": "Naha sightseeing",
             "detail": "Shuri Castle, Kokusai-dori, the Tsuboya pottery district.", "tag": "city"},
            {"date": d(2027, 3, 18), "title": "Churaumi Aquarium day-trip",
             "detail": "North-island day trip (rental car strongly preferred over bus, ~2h each way): "
                       "Churaumi Aquarium, Ocean Expo Park, Bise Fukugi Tree Road.", "tag": "tourist"},
            {"date": d(2027, 3, 19), "title": "Kerama Islands day-trip",
             "detail": "Ferry from Naha's Tomari Port to Zamami/Aka (50-70 min). Snorkelling at Furuzamami "
                       "Beach — and March is actually within Kerama whale-watching season.", "tag": "tourist"},
        ]},
        {"name": "Ishigaki & the Yaeyama Islands", "blurb": "The \"other really cool option\" — a genuinely "
                                                              "different Okinawa: turquoise water, jungle, and "
                                                              "a traditional buffalo-cart village.", "days": [
            {"date": d(2027, 3, 20), "title": "Naha → Ishigaki",
             "detail": "~1h domestic flight south to the Yaeyama Islands.", "tag": "travel"},
            {"date": d(2027, 3, 21), "title": "Ishigaki sightseeing",
             "detail": "Kabira Bay (glass-bottom boat over the coral), Ishigaki town.", "tag": "tourist"},
            {"date": d(2027, 3, 22), "title": "Iriomote Island day-trip",
             "detail": "Jungle kayaking/mangrove river, waterfalls — Japan's closest thing to a rainforest.",
             "tag": "tourist"},
            {"date": d(2027, 3, 23), "title": "Taketomi Island day-trip",
             "detail": "Traditional buffalo-cart village, red-tile roofs, white coral-sand streets — a step "
                       "back in time, 10 min by ferry from Ishigaki.", "tag": "tourist"},
            {"date": d(2027, 3, 24), "title": "Ishigaki free day",
             "detail": "Beach day / dive or snorkel trip — the payoff day, nothing scheduled.", "tag": "tourist"},
        ]},
        {"name": "Wind down & travel home", "blurb": "Includes one deliberate weather/ferry contingency day — "
                                                       "island-hopping itineraries always want one.", "days": [
            {"date": d(2027, 3, 25), "title": "Ishigaki → Naha",
             "detail": "Fly back to Naha, last-night shopping and okinawa soba.", "tag": "travel"},
            {"date": d(2027, 3, 26), "title": "Naha — final day",
             "detail": "Souvenirs, Tsuboya pottery, pack up.", "tag": "tourist"},
            {"date": d(2027, 3, 27), "title": "Contingency / buffer day",
             "detail": "Deliberately unscheduled — absorbs any flight/ferry weather delay from the island-hopping "
                       "leg. If nothing's gone wrong, an easy extra beach afternoon.", "tag": "tourist"},
            {"date": d(2027, 3, 28), "title": "Fly home", "detail": "Depart Japan.", "tag": "travel"},
        ]},
    ]
    ndays = sum(len(l["days"]) for l in legs)
    return {"meta": {"title": "Japan Trip 2027", "start": d(2027, 2, 27), "end": d(2027, 3, 28),
                     "days": ndays,
                     "note": "Osaka → Kyoto/Nara → Tokyo Marathon → Sendai/Matsushima → Niseko → Sapporo → "
                             "Okinawa (Naha + Kerama) → Ishigaki/Yaeyama Islands. Extended to a 4th week with "
                             "Okinawa added at the end. Note: the Osaka Grand Sumo tournament (~13-28 Mar 2027) "
                             "overlaps this trip's dates but not the Osaka leg itself (we're in Kansai 1-5 Mar) — "
                             "a known trade-off, not an oversight. Cherry blossoms are a coin-flip: current "
                             "estimate has peak bloom ~28 Mar-5 Apr, right at/after this trip's end — needs "
                             "reconfirming closer to the time if that matters."},
            "legs": legs}
