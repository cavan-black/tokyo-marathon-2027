"""Japan trip itinerary — Tokyo (race week incl. Ghibli Museum, snow monkeys & Golden
Gai), Shibuya/Harajuku the day after the race, the Nakasendo Trail (Magome-Tsumago)
between Tokyo and Kyoto, Kyoto/Nara (incl. a Fushimi sake brewery), Osaka (incl. NPB
preseason baseball), Niseko, Sapporo, Miyazaki (Kyushu) on the way south, then
Okinawa/Ishigaki. build() -> trip dict.

Route (27 Feb - 31 Mar 2027, 33 days): Tokyo race week (Ghibli Museum, Golden Gai on the
Monday — 6 days clear of the race so no need to hold back, snow monkeys day trip to
Jigokudani/Nagano) -> RACE -> Shibuya/Harajuku the day after (moved here on request) ->
a night on the Nakasendo Trail -> 3 days Kyoto/Nara (incl. a Fushimi sake brewery) ->
3 days Osaka (incl. NPB preseason baseball) -> Niseko -> Sapporo -> Miyazaki (1 night,
inserted here specifically because it has good direct flights to/from Osaka AND Naha but
nothing useful to Hokkaido, so this is the lowest-backtrack slot) -> Okinawa (Naha/Kerama,
incl. a proper night out) -> Ishigaki -> home. Sendai/Matsushima dropped in favour of the
extra Kyoto/Osaka day each. Note the pre-race Tokyo week is still exactly 7 days (Shibuya
moving out and snow monkeys moving in cancel out) — the one extra day in the whole trip is
Shibuya's new post-race slot, so the trip start stays at 27 Feb; only the END date moved,
from 30 to 31 Mar."""
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
            {"date": d(2027, 3, 1), "title": "Shinjuku by night — Golden Gai",
             "detail": "Shinjuku's Golden Gai and Omoide Yokocho for a proper night out — one of Tokyo's best "
                       "nightlife pockets. Deliberately on the Monday: 6 days clear of the race instead of 2, so "
                       "there's no need to hold back.", "tag": "city"},
            {"date": d(2027, 3, 2), "title": "Snow monkeys — Jigokudani, Nagano",
             "detail": "Jigokudani Monkey Park (Yudanaka): wild Japanese macaques bathing in hot springs, one of "
                       "Japan's most famous wildlife sights. Hokuriku Shinkansen Tokyo→Nagano (~1h20-1h30), then "
                       "the Nagano Dentetsu line to Yudanaka (~45min-1h), then a short bus/taxi + ~30 min forest "
                       "walk to the park. A long day (~10-12h door to door) but a genuine highlight, and a good "
                       "low-intensity day the morning after a big night out. Race is still 5 days out.",
             "tag": "tourist"},
            {"date": d(2027, 3, 3), "title": "Asakusa & Senso-ji",
             "detail": "Senso-ji temple, Nakamise shopping street, Sumida river walk.", "tag": "city"},
            {"date": d(2027, 3, 4), "title": "Ghibli Museum, Mitaka",
             "detail": "Studio Ghibli Museum + a wander through Inokashira Park and Kichijoji town. BOOK EARLY: "
                       "tickets are timed-entry, released monthly (typically the 10th, ~1-3 months ahead) and "
                       "sell out fast — this is the one thing on the whole trip that needs a calendar reminder "
                       "well before 2027.", "tag": "city"},
            {"date": d(2027, 3, 5), "title": "Expo & bib pickup",
             "detail": "Collect race kit, carb-load begins.", "tag": "city"},
            {"date": d(2027, 3, 6), "title": "Shakeout & rest",
             "detail": "Short shakeout + strides, full carb-load, lay out kit, early night.", "tag": "rest"},
        ]},
        {"name": "Race day", "blurb": "", "days": [
            {"date": d(2027, 3, 7), "title": "🏁 TOKYO MARATHON",
             "detail": "Race day. Then eat, drink (in moderation) and celebrate.", "tag": "race"},
        ]},
        {"name": "Tokyo — after the race", "blurb": "One more Tokyo day before heading out — legs are trashed, "
                                                       "so keep it to easy walking, people-watching, and sitting "
                                                       "down to drive things.", "days": [
            {"date": d(2027, 3, 8), "title": "Shibuya, Harajuku & street go-karting",
             "detail": "Shibuya Crossing, Harajuku's Takeshita Street, teamLab (Planets or Borderless) if tickets "
                       "allow. Then real-life Mario Kart: public-road go-karting through Tokyo in costume — the "
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
        {"name": "Kyoto & Nara", "blurb": "Three days now instead of two (traded for Sendai/Matsushima) — "
                                           "temples, a sake brewery, and Nara's Omizutori fire ritual if timing "
                                           "allows (1-14 Mar).", "days": [
            {"date": d(2027, 3, 11), "title": "Kyoto sightseeing",
             "detail": "Fushimi Inari, Gion, Kiyomizu-dera.", "tag": "city"},
            {"date": d(2027, 3, 12), "title": "Fushimi sake brewery",
             "detail": "Fushimi is Kyoto's historic sake-brewing district (40+ breweries, famously soft water). "
                       "Gekkeikan Okura Sake Museum for the history + tasting, Kizakura Kappa Country as a second "
                       "stop, and a walk along the willow-lined Fushimi canal past the old sake warehouses — "
                       "right next to Fushimi Inari, so it pairs naturally with yesterday.", "tag": "city"},
            {"date": d(2027, 3, 13), "title": "Nara day-trip — Omizutori",
             "detail": "Todai-ji + the Omizutori fire ritual (torches on the temple veranda each evening, "
                       "runs 1-14 Mar — check that year's exact times).", "tag": "city"},
        ]},
        {"name": "Osaka", "blurb": "Three days now instead of two — castle, baseball, and some of Japan's best "
                                    "nightlife.", "days": [
            {"date": d(2027, 3, 14), "title": "Osaka Castle & Dotonbori",
             "detail": "Osaka Castle in the afternoon, then Dotonbori for a street-food crawl "
                       "(takoyaki, okonomiyaki, kushikatsu) once the neon's on.", "tag": "city"},
            {"date": d(2027, 3, 15), "title": "Namba & Shinsekai by night",
             "detail": "Namba's bars and arcades, Shinsekai's retro streets and Tsutenkaku tower — Osaka's "
                       "nightlife is a genuine highlight, not an afterthought.", "tag": "city"},
            {"date": d(2027, 3, 16), "title": "NPB baseball & boat racing",
             "detail": "NPB preseason (\"open-sen\") games run into ~22 Mar — catch the Orix Buffaloes at Kyocera "
                       "Dome (in the city, most convenient) or the Hanshin Tigers at Koshien Stadium (short "
                       "Hanshin Line ride). Bonus: Spring Koshien, the high-school tournament at the same "
                       "stadium, typically runs ~19-31 Mar — tantalisingly close to these dates; push Osaka a "
                       "few days later if you'd rather catch that instead. FOR A FLUTTER: Boat Race Suminoe "
                       "(kyotei) runs near-daily, cash betting, English signage, no ID/account needed — 3 min "
                       "walk from Suminoekoen Station. The reliable bet regardless of the baseball/Koshien "
                       "calendar. Also worth checking closer to the time: Hanshin (Nishinomiya) or Kyoto "
                       "Racecourse — JRA horse racing alternates between the two most Sat/Sundays in season, "
                       "so there's a decent chance of a meeting on the Sunday (14 Mar).", "tag": "city"},
        ]},
        {"name": "To Niseko", "blurb": "A full travel day, not a quick hop — budget for it.", "days": [
            {"date": d(2027, 3, 17), "title": "Osaka → Niseko",
             "detail": "Fly Kansai (KIX) → New Chitose (~2.5h), then intercity bus to Niseko (~2.5-3h via "
                       "Rusutsu) — ~6.5-7.5h door to door. Shinkansen isn't competitive on this route; flying "
                       "is unambiguously the better option.", "tag": "travel"},
        ]},
        {"name": "Niseko — snowboarding", "blurb": "A few days on the mountain.", "days": [
            {"date": d(2027, 3, 18), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 19), "title": "Snowboarding", "detail": "Full day on the mountain.", "tag": "snow"},
            {"date": d(2027, 3, 20), "title": "Snowboarding", "detail": "Last day riding.", "tag": "snow"},
        ]},
        {"name": "Sapporo", "blurb": "Clock Tower by day, Susukino — one of Japan's biggest entertainment "
                                      "districts — by night. No racing here though: Sapporo Racecourse is "
                                      "summer-only (roughly late Jul-early Sep) and closed in March.", "days": [
            {"date": d(2027, 3, 21), "title": "Niseko → Sapporo",
             "detail": "Transfer to Sapporo. Clock Tower, Odori Park, Nijo Market.", "tag": "city"},
            {"date": d(2027, 3, 22), "title": "Susukino by night",
             "detail": "Ramen alley, izakayas, bars — Susukino is Hokkaido's nightlife capital. (No gambling "
                       "detour worth it near here: Obihiro's unique Banei Keiba — draft horses pulling sleds, "
                       "only venue of its kind in the world — is ~2h15-2h45 each way by JR, a full day round "
                       "trip. A genuine curiosity if it's a bucket-list item, but not worth it for a 2-day stop.)",
             "tag": "city"},
        ]},
        {"name": "Miyazaki", "blurb": "One night, inserted here on purpose: Miyazaki has no useful Hokkaido "
                                       "link, but good direct flights to both Osaka (~1h) and Naha (~1h37m) — "
                                       "this is the lowest-backtrack place in the whole route to fit it in.", "days": [
            {"date": d(2027, 3, 23), "title": "Sapporo → Miyazaki",
             "detail": "Connects via Osaka (Itami) or Haneda — a long travel day, arriving Miyazaki in the "
                       "evening.", "tag": "travel"},
            {"date": d(2027, 3, 24), "title": "Golf — Phoenix Country Club",
             "detail": "THE nice round: home of the Dunlop Phoenix Tournament (JGTO), 27 holes along the "
                       "Hitotsuba pine coast, ranked among Japan's top courses. Members-club in name but "
                       "visitors are genuinely welcome — book via GDO/Rakuten GORA/Jalan golf, or ask the "
                       "Sheraton Grande Ocean Resort/Seagaia concierge next door. Green fee ≈¥31,000-58,000 "
                       "(≈€190-350) depending on day/season; caddie is compulsory (adds to cost), jacket needed "
                       "in the clubhouse outside summer. ~20 min from JR Miyazaki Station/the airport. Given the "
                       "compulsory caddie pace + clubhouse time it eats most of a day — that's why Miyazaki got "
                       "a 3rd day rather than squeezing this in alongside Aoshima.", "tag": "tourist"},
            {"date": d(2027, 3, 25), "title": "Aoshima Shrine & on to Naha",
             "detail": "Aoshima Shrine and the \"Devil's Washboard\" (Oni no Sentakuita) tide-carved rock "
                       "formations, an easy couple of hours near the city. (Takachiho Gorge is ~2.5h further "
                       "with no train access — skipped to keep this a single efficient stop; would need its own "
                       "overnight to do properly.) Fly on to Naha in the afternoon/evening.", "tag": "tourist"},
        ]},
        {"name": "Okinawa — Naha & Kerama", "blurb": "Trimmed down and spread out rather than 12 days in one "
                                                       "block. March suits sightseeing/snorkelling more than "
                                                       "full beach season (water ~22°C). 4th day added for a "
                                                       "good-value round of golf.", "days": [
            {"date": d(2027, 3, 26), "title": "Naha — a proper night out",
             "detail": "Shuri Castle by day. By night: Kokusai-dori's main strip, or for something more local, "
                       "Sakaemachi Market (15 min walk / one monorail stop to Asato) — tiny hole-in-the-wall "
                       "izakayas threaded between market stalls, awamori and ¥300 yakitori, comes alive after "
                       "6pm, mostly no English menus. The better night out of the two.", "tag": "city"},
            {"date": d(2027, 3, 27), "title": "Golf — Okinawa Country Club",
             "detail": "The good-value round: ~15-20 min taxi from Naha (Nishihara). Green fee ≈¥12,000-18,000 "
                       "(≈€75-110, official-site discounts knock off ¥500-1,000). Club rental from ¥5,500, "
                       "shoes ¥1,100 — no need to bring clubs. No handicap certificate required; that's an old "
                       "private-club norm, not a real barrier for visitor/resort play in Japan anymore.",
             "tag": "tourist"},
            {"date": d(2027, 3, 28), "title": "Churaumi Aquarium day-trip",
             "detail": "North-island day trip (rental car preferred): Churaumi Aquarium, Ocean Expo Park, "
                       "Bise Fukugi Tree Road.", "tag": "tourist"},
            {"date": d(2027, 3, 29), "title": "Kerama Islands day-trip",
             "detail": "Ferry to Zamami/Aka (50-70 min). Snorkelling at Furuzamami Beach — March is within "
                       "Kerama whale-watching season.", "tag": "tourist"},
        ]},
        {"name": "Ishigaki taste", "blurb": "A compact 2 days rather than a full extra region — the \"other "
                                             "really cool option\" without over-extending the Okinawa block.", "days": [
            {"date": d(2027, 3, 30), "title": "Naha → Ishigaki",
             "detail": "~1h domestic flight south to the Yaeyama Islands.", "tag": "travel"},
            {"date": d(2027, 3, 31), "title": "Kabira Bay & Taketomi Island",
             "detail": "Morning: Kabira Bay glass-bottom boat. Afternoon: Taketomi Island (10 min ferry) — "
                       "buffalo-cart village, red-tile roofs, white coral-sand streets.", "tag": "tourist"},
        ]},
        {"name": "Travel home", "blurb": "", "days": [
            {"date": d(2027, 4, 1), "title": "Ishigaki → Naha",
             "detail": "Fly back to Naha to connect for the international leg home.", "tag": "travel"},
            {"date": d(2027, 4, 2), "title": "Fly home", "detail": "Depart Japan.", "tag": "travel"},
        ]},
    ]
    ndays = sum(len(l["days"]) for l in legs)
    return {"meta": {"title": "Japan Trip 2027", "start": d(2027, 2, 27), "end": d(2027, 4, 2),
                     "days": ndays,
                     "note": "Tokyo (race week: Golden Gai on the Monday, snow monkeys day trip, Ghibli Museum) "
                             "-> RACE -> Shibuya/Harajuku + go-karting the day after -> a night on the Nakasendo "
                             "Trail (Magome-Tsumago) -> 3 days Kyoto/Nara (incl. Fushimi sake brewery) -> 3 days "
                             "Osaka (incl. NPB baseball + Boat Race Suminoe) -> Niseko -> Sapporo -> Miyazaki "
                             "(3 nights, incl. golf at Phoenix Country Club) -> Okinawa (4 nights, incl. golf at "
                             "Okinawa Country Club) -> Ishigaki taste -> home. Sendai/Matsushima dropped in "
                             "favour of the extra Kyoto/Osaka day each. Miyazaki and Naha each grew by a day to "
                             "fit a round of golf properly (compulsory-caddie rounds eat most of a day) rather "
                             "than compressing them into already-packed sightseeing days — 35 days total now "
                             "(was 33), end date pushed from 31 Mar to 2 Apr. Silver lining: that now sits "
                             "squarely inside the ~28 Mar-5 Apr estimated cherry blossom peak-bloom window "
                             "(still a coin-flip 8+ months out — reconfirm closer to the time, but the odds just "
                             "improved). Ghibli Museum tickets (4 Mar) need booking ~1-3 months ahead, and the "
                             "go-karting needs an International Driving Permit sorted before departure — the "
                             "two hard deadlines here."},
            "legs": legs, "budget": budget()}


def budget():
    return {
        "intro": "Per person, 2 people sharing rooms, departing Málaga. FX rate used: 1 EUR ≈ ¥185.5 "
                 "(current). Costed for the full 35-day route (Miyazaki + snow monkeys + the extra Kyoto/Osaka "
                 "days + a golf day each in Miyazaki and Naha) — includes the Sapporo->Miyazaki->Naha flight "
                 "chain, the Tokyo->Nagano->Yudanaka rail round trip, the sake brewery/baseball tickets, and "
                 "both green fees. The Middle column is anchored on live-researched current prices (flights, JR "
                 "fares, hotel/lift-pass/green fee rates); Bare minimum and Luxury are reasoned extrapolations "
                 "using standard hostel/ryokan/business-class ratios — worth re-checking closer to booking "
                 "rather than treating as independently sourced.",
        "tiers": {"headers": ["Tier", "What it gets you"], "rows": [
            ["Bare minimum", "Hostel dorms/capsules, conbini + casual meals, budget/no-frills flights, self-guided everything."],
            ["Middle", "Business hotels, casual-to-mid restaurants, standard economy flights — the itinerary as planned."],
            ["Luxury", "5★ hotels/luxury ryokan (kaiseki dinners included), business class flights, private tours/guides, fine dining."],
        ]},
        "table": {"headers": ["Category", "Bare minimum", "Middle", "Luxury"], "rows": [
            ["Int'l flights (Málaga↔Naha, open-jaw)", "€700", "€975", "€3,900"],
            ["Domestic rail (incl. Nagano/snow monkeys)", "€160", "€235", "€420"],
            ["Domestic flights (incl. Sapporo→Miyazaki→Naha chain)", "€280", "€415", "€800"],
            ["Accommodation (34 nights)", "€820", "€1,275", "€8,200"],
            ["Niseko lift passes (3 days)", "€200", "€200", "€200"],
            ["Food / local transport / incidentals (35 days)", "€1,870", "€2,535", "€7,000"],
            ["Golf (Phoenix CC + Okinawa CC, incl. caddie/rental)", "€290", "€350", "€500"],
            ["Other activities & tours (sake brewery, baseball/boat racing, Aoshima, go-karting)", "€135", "€190", "€1,000"],
        ]},
        "durations": {"headers": ["Duration", "Bare minimum", "Middle", "Luxury"], "rows": [
            ["Full itinerary (35 days, 27 Feb-2 Apr)", "≈€4,450", "≈€6,200", "≈€22,000"],
            ["3-week (~23 days)*", "≈€3,300", "≈€4,200", "≈€16,000"],
        ]},
        "notes": [
            "*3-week = drop Miyazaki (and its Phoenix CC round) and the Ishigaki extension entirely, and trim "
            "Tokyo (8→6 nights, keep the snow monkeys, drop nothing else), Naha (4→2, keeping the Okinawa CC "
            "round since it's cheap and easy) — same core route, tighter stays. The cheap add-ons (sake "
            "brewery, baseball, boat racing) stay in even at 3 weeks since they cost almost nothing extra.",
            "The swing between tiers is almost entirely flights and accommodation — food and activities "
            "barely move the needle by comparison.",
            "Golf is two fixed-price rounds, not really tier-scalable — Phoenix Country Club (Miyazaki, the "
            "splurge round: ¥31,000-58,000/≈€190-350 green fee depending on day/season, compulsory caddie) and "
            "Okinawa Country Club (Naha, the good-value round: ¥12,000-18,000/≈€75-110, club rental from "
            "¥5,500). The Luxury figure assumes premium-date booking + better caddie tip, not a different course.",
            "Niseko lift passes are essentially fixed regardless of tier (it's a set resort rate) — "
            "€200 pp for a 3-day pass (¥36,800 regular-season rate, official niseko.ne.jp pricing, "
            "checked 2026). Niseko/Hakuba lift prices have risen ~30-40% over the last ~2 years — mostly "
            "resorts pricing to heavy international demand (80-90% of Niseko visitors are foreign), not "
            "just yen weakness — so re-verify this closer to booking, it moves fast.",
            "The Miyazaki insertion is the single biggest domestic-flight cost driver here — three short hops "
            "(Sapporo→Osaka/Haneda→Miyazaki→Naha) instead of one direct Sendai→Naha routing from the earlier "
            "version. Worth knowing that's what you're paying for the detour.",
            "The luxury total is dominated by business-class flights (~4x economy) and 34 nights of "
            "5★/ryokan. \"Luxury lodging but economy flights\" comes out to roughly €9,700–11,300 pp — a "
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
