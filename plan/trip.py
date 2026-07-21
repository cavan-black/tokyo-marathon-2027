"""Japan trip itinerary — Tokyo (race week), Kyoto/Nara, Osaka, Niseko, Sapporo,
Sendai/Matsushima on the way back south, then Okinawa/Ishigaki. build() -> trip dict.

Route (27 Feb - 28 Mar 2027, 30 days): arrive & stay in Tokyo for race week -> RACE ->
day after, to Kyoto -> a couple of days there -> a couple of days Osaka -> Niseko ->
Sapporo -> back down through Sendai/Matsushima -> Okinawa (trimmed from the earlier
12-day version down to ~7 days, still covering Naha/Kerama + a taste of Ishigaki) ->
home. Nightlife stops folded in at Tokyo (Shinjuku), Osaka (Dotonbori/Namba), Sapporo
(Susukino) and Naha (Kokusai-dori) — some of Japan's best-known nightlife districts."""
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
            {"date": d(2027, 3, 3), "title": "Tsukiji & Ginza",
             "detail": "Tsukiji Outer Market for breakfast/lunch, Ginza for a wander.", "tag": "city"},
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
        {"name": "To Kyoto", "blurb": "Straight out the day after — legs will thank you for the train, not more walking.", "days": [
            {"date": d(2027, 3, 8), "title": "Tokyo → Kyoto",
             "detail": "Shinkansen the day after the race. Recovery-mode legs, easy check-in.", "tag": "travel"},
        ]},
        {"name": "Kyoto & Nara", "blurb": "A couple of days — temples, and Nara's Omizutori fire ritual if timing allows (1-14 Mar).", "days": [
            {"date": d(2027, 3, 9), "title": "Kyoto sightseeing",
             "detail": "Fushimi Inari, Gion, Kiyomizu-dera.", "tag": "city"},
            {"date": d(2027, 3, 10), "title": "Nara day-trip — Omizutori",
             "detail": "Todai-ji + the Omizutori fire ritual (torches on the temple veranda each evening, "
                       "runs 1-14 Mar — check that year's exact times).", "tag": "city"},
        ]},
        {"name": "Osaka", "blurb": "A couple of days — castle by day, some of Japan's best nightlife by night.", "days": [
            {"date": d(2027, 3, 11), "title": "Osaka Castle & Dotonbori",
             "detail": "Osaka Castle in the afternoon, then Dotonbori for a street-food crawl "
                       "(takoyaki, okonomiyaki, kushikatsu) once the neon's on.", "tag": "city"},
            {"date": d(2027, 3, 12), "title": "Namba & Shinsekai by night",
             "detail": "Namba's bars and arcades, Shinsekai's retro streets and Tsutenkaku tower — Osaka's "
                       "nightlife is a genuine highlight, not an afterthought.", "tag": "city"},
        ]},
        {"name": "To Niseko", "blurb": "Long travel day, west coast to Hokkaido.", "days": [
            {"date": d(2027, 3, 13), "title": "Osaka → Niseko",
             "detail": "Shinkansen/flight combo up to Hokkaido, then transfer to Niseko.", "tag": "travel"},
        ]},
        {"name": "Niseko — snowboarding", "blurb": "A few days on the mountain.", "days": [
            {"date": d(2027, 3, 14), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 15), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 16), "title": "Snowboarding", "detail": "Last day riding.", "tag": "snow"},
        ]},
        {"name": "Sapporo", "blurb": "Clock Tower by day, Susukino — one of Japan's biggest entertainment "
                                      "districts — by night.", "days": [
            {"date": d(2027, 3, 17), "title": "Niseko → Sapporo",
             "detail": "Transfer to Sapporo. Clock Tower, Odori Park, Nijo Market.", "tag": "city"},
            {"date": d(2027, 3, 18), "title": "Susukino by night",
             "detail": "Ramen alley, izakayas, bars — Susukino is Hokkaido's nightlife capital.", "tag": "city"},
        ]},
        {"name": "Sendai & Matsushima", "blurb": "Heading back south — directly on the Tohoku Shinkansen, "
                                                   "and Matsushima Bay is one of Japan's official Three Views.", "days": [
            {"date": d(2027, 3, 19), "title": "Sapporo → Sendai",
             "detail": "Hokkaido Shinkansen back down via Shin-Hakodate-Hokuto/Shin-Aomori to Sendai.", "tag": "travel"},
            {"date": d(2027, 3, 20), "title": "Matsushima day-trip",
             "detail": "~40 min local train from Sendai. Boat cruise through the pine-covered islets.", "tag": "city"},
        ]},
        {"name": "Okinawa — Naha & Kerama", "blurb": "Trimmed down and spread out rather than 12 days in one "
                                                       "block. March suits sightseeing/snorkelling more than "
                                                       "full beach season (water ~22°C).", "days": [
            {"date": d(2027, 3, 21), "title": "Sendai → Naha",
             "detail": "Fly south (likely connecting via Tokyo). Warm evening, ease in.", "tag": "travel"},
            {"date": d(2027, 3, 22), "title": "Naha by night",
             "detail": "Shuri Castle by day, Kokusai-dori's bars and izakayas by night.", "tag": "city"},
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
                     "note": "Tokyo (race week) -> RACE -> Kyoto/Nara -> Osaka -> Niseko -> Sapporo -> "
                             "Sendai/Matsushima (heading back south) -> Okinawa (Naha/Kerama) -> Ishigaki taste "
                             "-> home. Okinawa trimmed from ~12 days down to ~7, with nightlife stops folded in "
                             "at Tokyo (Shinjuku), Osaka (Dotonbori/Namba), Sapporo (Susukino) and Naha "
                             "(Kokusai-dori). Note: the Osaka Grand Sumo tournament (~13-28 Mar 2027) overlaps "
                             "this trip's dates but not the Osaka leg itself (we're there 11-12 Mar) — a known "
                             "trade-off. Cherry blossoms are a coin-flip: current estimate has peak bloom "
                             "~28 Mar-5 Apr, right at/after this trip's end — reconfirm closer to the time."},
            "legs": legs}
