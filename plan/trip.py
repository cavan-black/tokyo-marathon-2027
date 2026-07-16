"""Japan trip itinerary — Kyoto, Tokyo Marathon, Niseko, Sapporo. build() -> trip dict.
Draft — the 14-20 Mar block is a placeholder pending group decisions."""
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
        {"name": "Kyoto", "blurb": "A few days of temples, food and jet-lag walks before the taper kicks in.", "days": [
            {"date": d(2027, 2, 28), "title": "Arrive & settle",
             "detail": "Land, transfer to Kyoto, check in. Easy walking only — race is 7 days out.", "tag": "travel"},
            {"date": d(2027, 3, 1), "title": "Kyoto sightseeing",
             "detail": "Fushimi Inari, Gion, Kiyomizu-dera.", "tag": "city"},
            {"date": d(2027, 3, 2), "title": "Kyoto sightseeing",
             "detail": "Arashiyama bamboo grove, Kinkaku-ji, Nishiki Market.", "tag": "city"},
            {"date": d(2027, 3, 3), "title": "Kyoto free day",
             "detail": "Nara day-trip (deer park) or a slow Kyoto day — keep it easy, no big hikes this close to race day.",
             "tag": "city"},
        ]},
        {"name": "To Tokyo", "blurb": "Shinkansen across, into race week.", "days": [
            {"date": d(2027, 3, 4), "title": "Kyoto → Tokyo",
             "detail": "Shinkansen to Tokyo, check in, easy shakeout jog to loosen up after travel.", "tag": "travel"},
        ]},
        {"name": "Tokyo — race week", "blurb": "Expo, carb-load, keep it low-key.", "days": [
            {"date": d(2027, 3, 5), "title": "Expo & bib pickup",
             "detail": "Collect race kit, light sightseeing (Shibuya/Harajuku), carb-load begins.", "tag": "city"},
            {"date": d(2027, 3, 6), "title": "Shakeout & rest",
             "detail": "Short shakeout + strides, full carb-load, lay out race kit, early night.", "tag": "rest"},
        ]},
        {"name": "Race day", "blurb": "", "days": [
            {"date": d(2027, 3, 7), "title": "🏁 TOKYO MARATHON",
             "detail": "Race day. Then eat, drink (in moderation) and celebrate.", "tag": "race"},
        ]},
        {"name": "Tokyo recovery", "blurb": "One full day off your feet before the next leg.", "days": [
            {"date": d(2027, 3, 8), "title": "Recovery day",
             "detail": "Legs up, short walk only, onsen/massage if you can find one, eat properly.", "tag": "rest"},
        ]},
        {"name": "To Niseko", "blurb": "Flight + transfer up to Hokkaido.", "days": [
            {"date": d(2027, 3, 9), "title": "Tokyo → Niseko",
             "detail": "Fly Haneda/Narita → New Chitose, ~2.5h transfer bus to Niseko. Gear rental, easy first runs if there's time.",
             "tag": "travel"},
        ]},
        {"name": "Niseko — snowboarding", "blurb": "A few days on the mountain.", "days": [
            {"date": d(2027, 3, 10), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 11), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 12), "title": "Snowboarding", "detail": "Last day riding.", "tag": "snow"},
        ]},
        {"name": "Sapporo", "blurb": "A day in the city on the way through.", "days": [
            {"date": d(2027, 3, 13), "title": "Niseko → Sapporo",
             "detail": "Transfer to Sapporo. Clock Tower, Odori Park, Nijo Market, ramen alley.", "tag": "city"},
        ]},
        {"name": "Tourist stuff — TBD",
         "blurb": "Placeholder days — fill these in once the group decides (Otaru, Hakone, Nikko, back to Tokyo, etc.).",
         "days": [
            {"date": d(2027, 3, 14), "title": "Flexible",
             "detail": "TBD — Otaru day-trip (canal, glassblowing) or more Sapporo.", "tag": "tourist"},
            {"date": d(2027, 3, 15), "title": "Flexible",
             "detail": "TBD — head back toward Tokyo, or more Hokkaido.", "tag": "tourist"},
            {"date": d(2027, 3, 16), "title": "Flexible",
             "detail": "TBD — Hakone or Nikko day-trip from Tokyo.", "tag": "tourist"},
            {"date": d(2027, 3, 17), "title": "Flexible",
             "detail": "TBD — Tokyo neighbourhoods: Asakusa, Akihabara, Odaiba.", "tag": "tourist"},
            {"date": d(2027, 3, 18), "title": "Flexible", "detail": "TBD — free day / shopping / onsen.", "tag": "tourist"},
            {"date": d(2027, 3, 19), "title": "Flexible", "detail": "TBD — free day.", "tag": "tourist"},
            {"date": d(2027, 3, 20), "title": "Pack up", "detail": "Last-minute shopping, final dinner.", "tag": "tourist"},
        ]},
        {"name": "Travel home", "blurb": "", "days": [
            {"date": d(2027, 3, 21), "title": "Fly home", "detail": "Depart Japan.", "tag": "travel"},
        ]},
    ]
    ndays = sum(len(l["days"]) for l in legs)
    return {"meta": {"title": "Japan Trip 2027", "start": d(2027, 2, 27), "end": d(2027, 3, 21),
                     "days": ndays,
                     "note": "Draft itinerary — Kyoto → Tokyo Marathon → Niseko → Sapporo. "
                             "The 14–20 Mar block is a placeholder; fill in once decided."},
            "legs": legs}
