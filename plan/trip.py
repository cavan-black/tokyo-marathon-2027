"""Japan trip itinerary — Tokyo (race week, incl. Ghibli Museum), the Nakasendo Trail
(Magome-Tsumago) between Tokyo and Kyoto, Kyoto/Nara, Osaka, Niseko, Sapporo,
Sendai/Matsushima on the way back south, then Okinawa/Ishigaki. build() -> trip dict.

Route (27 Feb - 28 Mar 2027, 30 days): arrive & stay in Tokyo for race week (incl. the
Ghibli Museum) -> RACE -> day after, a night on the old Nakasendo Trail (Magome to
Tsumago) on the way to Kyoto -> a couple of days Kyoto/Nara -> a couple of days Osaka ->
Niseko -> Sapporo -> back down through Sendai/Matsushima -> Okinawa (trimmed to ~6 days:
Naha/Kerama + a taste of Ishigaki) -> home. Nightlife stops folded in at Tokyo
(Shinjuku), Osaka (Dotonbori/Namba), Sapporo (Susukino) and Naha (Kokusai-dori)."""
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
            {"date": d(2027, 3, 1), "title": "Asakusa & Senso-ji",
             "detail": "Senso-ji temple, Nakamise shopping street, Sumida river walk.", "tag": "city"},
            {"date": d(2027, 3, 2), "title": "Shibuya & Harajuku",
             "detail": "Shibuya Crossing, Harajuku's Takeshita Street, teamLab (Planets or Borderless) if tickets allow.",
             "tag": "city"},
            {"date": d(2027, 3, 3), "title": "Ghibli Museum, Mitaka",
             "detail": "Studio Ghibli Museum + a wander through Inokashira Park and Kichijoji town. BOOK EARLY: "
                       "tickets are timed-entry, released monthly (typically the 10th, ~1-3 months ahead) and "
                       "sell out fast — this is the one thing on the whole trip that needs a calendar reminder "
                       "well before 2027. (Ghibli Park near Nagoya is a possible bolt-on to the Nakasendo travel "
                       "day below if you want more Ghibli — would need an extra day.)", "tag": "city"},
            {"date": d(2027, 3, 4), "title": "Expo & bib pickup",
             "detail": "Collect race kit, carb-load begins.", "tag": "city"},
            {"date": d(2027, 3, 5), "title": "Free day — Shinjuku by night",
             "detail": "Easy day, then Shinjuku's Golden Gai and Omoide Yokocho for a proper night out — "
                       "one of Tokyo's best nightlife pockets. Keep it sensible, race is 2 days out.", "tag": "city"},
            {"date": d(2027, 3, 6), "title": "Shakeout & rest",
             "detail": "Short shakeout + strides, full carb-load, lay out kit, early night.", "tag": "rest"},
        ]},
        {"name": "Race day", "blurb": "", "days": [
            {"date": d(2027, 3, 7), "title": "🏁 TOKYO MARATHON",
             "detail": "Race day. Then eat, drink (in moderation) and celebrate.", "tag": "race"},
        ]},
        {"name": "Nakasendo Trail — Magome to Tsumago", "blurb": "The old Edo-period highway between Tokyo and "
                                                                   "Kyoto — a night in a preserved post town and "
                                                                   "a forest walk between two of Japan's "
                                                                   "best-kept historic villages.", "days": [
            {"date": d(2027, 3, 8), "title": "Tokyo → Magome",
             "detail": "Shinkansen to Nagoya, limited express to Nakatsugawa, bus to Magome. Explore the post "
                       "town in the afternoon, overnight in a traditional minshuku. Recovery-mode legs, no rush.",
             "tag": "travel"},
            {"date": d(2027, 3, 9), "title": "Walk to Tsumago, on to Kyoto",
             "detail": "The Magome-Tsumago walk: ~7.8 km, ~2.5-3 h through forest, waterfalls and Edo-period "
                       "checkpoints — genuinely one of Japan's best short walks. Then bus/train to Nagiso, "
                       "limited express to Nagoya, shinkansen on to Kyoto by evening.", "tag": "city"},
        ]},
        {"name": "Kyoto & Nara", "blurb": "A couple of days — temples, and Nara's Omizutori fire ritual if timing allows (1-14 Mar).", "days": [
            {"date": d(2027, 3, 10), "title": "Kyoto sightseeing",
             "detail": "Fushimi Inari, Gion, Kiyomizu-dera.", "tag": "city"},
            {"date": d(2027, 3, 11), "title": "Nara day-trip — Omizutori",
             "detail": "Todai-ji + the Omizutori fire ritual (torches on the temple veranda each evening, "
                       "runs 1-14 Mar — check that year's exact times).", "tag": "city"},
        ]},
        {"name": "Osaka", "blurb": "A couple of days — castle by day, some of Japan's best nightlife by night.", "days": [
            {"date": d(2027, 3, 12), "title": "Osaka Castle & Dotonbori",
             "detail": "Osaka Castle in the afternoon, then Dotonbori for a street-food crawl "
                       "(takoyaki, okonomiyaki, kushikatsu) once the neon's on.", "tag": "city"},
            {"date": d(2027, 3, 13), "title": "Namba & Shinsekai by night",
             "detail": "Namba's bars and arcades, Shinsekai's retro streets and Tsutenkaku tower — Osaka's "
                       "nightlife is a genuine highlight, not an afterthought.", "tag": "city"},
        ]},
        {"name": "To Niseko", "blurb": "Long travel day, west coast to Hokkaido.", "days": [
            {"date": d(2027, 3, 14), "title": "Osaka → Niseko",
             "detail": "Shinkansen/flight combo up to Hokkaido, then transfer to Niseko.", "tag": "travel"},
        ]},
        {"name": "Niseko — snowboarding", "blurb": "A few days on the mountain.", "days": [
            {"date": d(2027, 3, 15), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 16), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 17), "title": "Snowboarding", "detail": "Last day riding.", "tag": "snow"},
        ]},
        {"name": "Sapporo", "blurb": "Clock Tower by day, Susukino — one of Japan's biggest entertainment "
                                      "districts — by night.", "days": [
            {"date": d(2027, 3, 18), "title": "Niseko → Sapporo",
             "detail": "Transfer to Sapporo. Clock Tower, Odori Park, Nijo Market.", "tag": "city"},
            {"date": d(2027, 3, 19), "title": "Susukino by night",
             "detail": "Ramen alley, izakayas, bars — Susukino is Hokkaido's nightlife capital.", "tag": "city"},
        ]},
        {"name": "Sendai & Matsushima", "blurb": "Heading back south — directly on the Tohoku Shinkansen, "
                                                   "and Matsushima Bay is one of Japan's official Three Views.", "days": [
            {"date": d(2027, 3, 20), "title": "Sapporo → Sendai",
             "detail": "Hokkaido Shinkansen back down via Shin-Hakodate-Hokuto/Shin-Aomori to Sendai.", "tag": "travel"},
            {"date": d(2027, 3, 21), "title": "Matsushima day-trip",
             "detail": "~40 min local train from Sendai. Boat cruise through the pine-covered islets.", "tag": "city"},
        ]},
        {"name": "Okinawa — Naha & Kerama", "blurb": "Trimmed down and spread out rather than 12 days in one "
                                                       "block. March suits sightseeing/snorkelling more than "
                                                       "full beach season (water ~22°C).", "days": [
            {"date": d(2027, 3, 22), "title": "Sendai → Naha",
             "detail": "Fly south (likely connecting via Tokyo). Shuri Castle if there's time, Kokusai-dori's "
                       "bars and izakayas by night.", "tag": "travel"},
            {"date": d(2027, 3, 23), "title": "Churaumi Aquarium day-trip",
             "detail": "North-island day trip (rental car preferred): Churaumi Aquarium, Ocean Expo Park, "
                       "Bise Fukugi Tree Road.", "tag": "tourist"},
            {"date": d(2027, 3, 24), "title": "Kerama Islands day-trip",
             "detail": "Ferry to Zamami/Aka (50-70 min). Snorkelling at Furuzamami Beach — March is within "
                       "Kerama whale-watching season.", "tag": "tourist"},
        ]},
        {"name": "Ishigaki taste", "blurb": "A compact 2 days rather than a full extra region — the \"other "
                                             "really cool option\" without over-extending the Okinawa block.", "days": [
            {"date": d(2027, 3, 25), "title": "Naha → Ishigaki",
             "detail": "~1h domestic flight south to the Yaeyama Islands.", "tag": "travel"},
            {"date": d(2027, 3, 26), "title": "Kabira Bay & Taketomi Island",
             "detail": "Morning: Kabira Bay glass-bottom boat. Afternoon: Taketomi Island (10 min ferry) — "
                       "buffalo-cart village, red-tile roofs, white coral-sand streets.", "tag": "tourist"},
        ]},
        {"name": "Travel home", "blurb": "", "days": [
            {"date": d(2027, 3, 27), "title": "Ishigaki → Naha",
             "detail": "Fly back to Naha to connect for the international leg home.", "tag": "travel"},
            {"date": d(2027, 3, 28), "title": "Fly home", "detail": "Depart Japan.", "tag": "travel"},
        ]},
    ]
    ndays = sum(len(l["days"]) for l in legs)
    return {"meta": {"title": "Japan Trip 2027", "start": d(2027, 2, 27), "end": d(2027, 3, 28),
                     "days": ndays,
                     "note": "Tokyo (race week + Ghibli Museum) -> RACE -> a night on the Nakasendo Trail "
                             "(Magome-Tsumago) -> Kyoto/Nara -> Osaka -> Niseko -> Sapporo -> Sendai/Matsushima "
                             "(heading back south) -> Okinawa (Naha/Kerama) -> Ishigaki taste -> home. Okinawa "
                             "trimmed from ~12 days down to ~6, with nightlife stops folded in at Tokyo "
                             "(Shinjuku), Osaka (Dotonbori/Namba), Sapporo (Susukino) and Naha (Kokusai-dori). "
                             "Note: the Osaka Grand Sumo tournament (~13-28 Mar 2027) overlaps this trip's dates "
                             "but not the Osaka leg itself (we're there 12-13 Mar) — a known trade-off. Cherry "
                             "blossoms are a coin-flip: current estimate has peak bloom ~28 Mar-5 Apr, right "
                             "at/after this trip's end — reconfirm closer to the time. Ghibli Museum tickets "
                             "(3 Mar) need booking ~1-3 months ahead — the one hard deadline in this itinerary."},
            "legs": legs, "budget": budget()}


def budget():
    return {
        "intro": "Per person, 2 people sharing rooms, departing Málaga. FX rate used: 1 EUR ≈ ¥185.5 "
                 "(current). The Middle column is built from live-researched current prices (flights, JR "
                 "fares, hotel/lift-pass rates); Bare minimum and Luxury are reasoned extrapolations from "
                 "that anchor using standard hostel/ryokan/business-class ratios — worth re-checking closer "
                 "to booking rather than treating as independently sourced.",
        "tiers": {"headers": ["Tier", "What it gets you"], "rows": [
            ["Bare minimum", "Hostel dorms/capsules, conbini + casual meals, budget/no-frills flights, self-guided everything."],
            ["Middle", "Business hotels, casual-to-mid restaurants, standard economy flights — the itinerary as planned."],
            ["Luxury", "5★ hotels/luxury ryokan (kaiseki dinners included), business class flights, private tours/guides, fine dining."],
        ]},
        "table": {"headers": ["Category", "Bare minimum", "Middle", "Luxury"], "rows": [
            ["Int'l flights (Málaga↔Naha, open-jaw)", "€700", "€975", "€3,900"],
            ["Domestic rail", "€150", "€225", "€400"],
            ["Domestic flights", "€180", "€265", "€550"],
            ["Accommodation", "€700", "€1,090", "€7,000"],
            ["Niseko lift passes (3 days)", "€200", "€200", "€200"],
            ["Food / local transport / incidentals", "€1,600", "€2,175", "€6,000"],
            ["Activities & tours (incl. private lessons/guide in Luxury)", "€85", "€120", "€850"],
        ]},
        "durations": {"headers": ["Duration", "Bare minimum", "Middle", "Luxury"], "rows": [
            ["4-week (30 days, full itinerary)", "≈€3,650", "≈€5,050", "≈€18,900"],
            ["3-week (~23 days)*", "≈€3,150", "≈€4,050", "≈€15,750"],
        ]},
        "notes": [
            "*3-week = drop the Ishigaki extension entirely, and trim Tokyo (7→5 nights), Naha (3→2), "
            "Sendai (2→1), and the Nakasendo stop (2→1 day) — same core route, tighter stays.",
            "The swing between tiers is almost entirely flights and accommodation — food and activities "
            "barely move the needle by comparison.",
            "Niseko lift passes are essentially fixed regardless of tier (it's a set resort rate) — "
            "€200 pp for a 3-day pass (¥36,800 regular-season rate, official niseko.ne.jp pricing, "
            "checked 2026). Niseko/Hakuba lift prices have risen ~30-40% over the last ~2 years — mostly "
            "resorts pricing to heavy international demand (80-90% of Niseko visitors are foreign), not "
            "just yen weakness — so re-verify this closer to booking, it moves fast.",
            "The luxury total is dominated by business-class flights (~4x economy) and 30 nights of "
            "5★/ryokan. \"Luxury lodging but economy flights\" comes out to roughly €8,000–9,500 pp — a "
            "more common real-world middle ground if the full luxury number is too steep.",
        ],
    }
