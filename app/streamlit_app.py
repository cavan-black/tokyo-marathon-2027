#!/usr/bin/env python3
"""Shared Tokyo Marathon dashboard — one tab per runner, planned vs actual, Strava-synced.
Visual design adapted from Stevie's "Sub-3:15 Build" single-page layout."""
import os, sys, json, html
from datetime import date, datetime

import pandas as pd
import streamlit as st

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, ROOT)

st.set_page_config(page_title="Tokyo 2027 · Team dashboard", page_icon="🏃", layout="wide")

# Wide layout stretches full browser width — cap it so there's breathing room on both sides.
# Streamlit renames/nests this container across versions, so target every known selector + !important.
st.markdown(
    """<style>
    .block-container, .stMainBlockContainer,
    div[data-testid="stAppViewContainer"] .main .block-container,
    div[data-testid="stMainBlockContainer"] {
        max-width: 1180px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }
    </style>""",
    unsafe_allow_html=True,
)

# ---- workout type -> chip class + label (mirrors Stevie's palette) ----
TYPE_LABEL = {"rest": "Rest", "recovery": "Recovery", "easy": "Easy", "long": "Long",
              "quality": "Quality", "race": "Race", "tt": "Time trial"}
TYPE_CLASS = {"rest": "t-rest", "recovery": "t-recovery", "easy": "t-easy", "long": "t-long",
              "quality": "t-quality", "race": "t-race", "tt": "t-quality"}
# progress status -> dot colour
STATUS_COLOR = {"Done": "var(--good)", "Partial": "var(--warn)", "Missed": "var(--accent)"}

STYLE = """<style>
.sv{--paper:#f6f5f2;--surface:#fff;--surface-2:#faf9f6;--ink:#191b21;--muted:#6b6e77;--faint:#9a9ca3;
  --line:#e5e3dc;--line-strong:#d6d3ca;--accent:#ce2e3b;--accent-ink:#ce2e3b;--accent-soft:rgba(206,46,59,.09);
  --pA:#4f7391;--pB:#2f8f7e;--pC:#bd7a2a;--pD:#8663ad;--good:#2f8f7e;--warn:#bd7a2a;--radius:13px;
  --font-mono:"Cascadia Code",ui-monospace,"SF Mono","Segoe UI Mono",Menlo,Consolas,monospace;}
@media (prefers-color-scheme:dark){.sv{--paper:#0e1014;--surface:#171a20;--surface-2:#14161b;--ink:#ecedf0;
  --muted:#9aa0ab;--faint:#6c7079;--line:#262a33;--line-strong:#333844;--accent:#f2545b;--accent-ink:#f97077;
  --accent-soft:rgba(242,84,91,.13);--pA:#7aa0bd;--pB:#4fb7a3;--pC:#d99a4e;--pD:#ac8bd0;--good:#4fb7a3;--warn:#d99a4e;}}
.sv{color:var(--ink);font-size:15px;line-height:1.5;}
.sv .mono{font-family:var(--font-mono);font-variant-numeric:tabular-nums;}
.sv .eyebrow{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--accent-ink);}
.sv h2{font-size:20px;font-weight:750;letter-spacing:-.01em;margin:0;}
.sv h3{font-size:15px;font-weight:700;margin:0 0 10px;}
.sv .sub{color:var(--muted);font-size:14.5px;margin:2px 0 0;}
.sv .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;margin:14px 0 4px;}
.sv .fact{background:var(--surface);padding:13px 16px;}
.sv .fact .k{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);}
.sv .fact .v{font-size:20px;font-weight:700;margin-top:3px;letter-spacing:-.01em;}
.sv .fact .v small{font-size:12px;font-weight:500;color:var(--muted);}
.sv .sec{padding:22px 0 6px;border-top:1px solid var(--line);margin-top:18px;}
.sv .sec-head{display:flex;align-items:baseline;gap:12px;margin-bottom:16px;flex-wrap:wrap;}
.sv .grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.sv .grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
@media (max-width:820px){.sv .grid2,.sv .grid3{grid-template-columns:1fr;}}
.sv .card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;}
.sv .card p{margin:0;font-size:14px;}
.sv table.data{width:100%;border-collapse:collapse;}
.sv table.data th,.sv table.data td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--line);}
.sv table.data th{font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--faint);font-weight:600;}
.sv table.data td.num{text-align:right;font-family:var(--font-mono);font-weight:600;font-variant-numeric:tabular-nums;}
.sv .zone-dot{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:8px;vertical-align:middle;}
.sv ul.tight{margin:0;padding-left:18px;}
.sv ul.tight li{margin:5px 0;font-size:14px;}
.sv .tmpl .row{display:grid;grid-template-columns:46px 1fr;gap:12px;padding:7px 0;border-bottom:1px solid var(--line);}
.sv .tmpl .row:last-child{border-bottom:0;}
.sv .tmpl .d{font-family:var(--font-mono);font-weight:700;color:var(--muted);font-size:13px;}
.sv .tmpl .s{font-size:13.5px;}
.sv .gates{display:flex;flex-direction:column;gap:9px;}
.sv .gate{display:grid;grid-template-columns:64px 1fr auto;gap:12px;align-items:center;padding:11px 14px;
  border:1px solid var(--line);border-radius:11px;background:var(--surface);}
.sv .gate.decisive{border-color:var(--accent);background:var(--accent-soft);}
.sv .gate .id{font-family:var(--font-mono);font-weight:700;font-size:15px;}
.sv .gate .id small{display:block;font-size:10px;color:var(--faint);font-weight:500;}
.sv .gate .what{font-weight:650;font-size:14px;}
.sv .gate .blurb{color:var(--muted);font-size:12.5px;}
.sv .gate .target{text-align:right;font-family:var(--font-mono);font-weight:700;font-size:14px;color:var(--accent-ink);}
.sv .badge-dec{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  color:var(--accent-ink);border:1px solid var(--accent);border-radius:20px;padding:1px 8px;margin-left:6px;}
.sv .legend{display:flex;flex-wrap:wrap;gap:8px 14px;margin:12px 0;}
.sv .legend span{font-size:12px;color:var(--muted);display:inline-flex;align-items:center;gap:6px;}
.sv .chip{display:inline-block;font-size:11px;font-weight:650;padding:1px 7px;border-radius:5px;white-space:nowrap;}
.sv .phase-group{margin-top:22px;}
.sv .phase-bar{display:flex;align-items:center;gap:12px;margin-bottom:10px;}
.sv .phase-tag{font-family:var(--font-mono);font-weight:700;font-size:12px;color:#fff;padding:3px 9px;border-radius:6px;}
.sv .phase-bar h3{font-size:16px;font-weight:750;margin:0;}
.sv .phase-bar .rng{color:var(--faint);font-size:12.5px;font-family:var(--font-mono);}
.sv details.week{border:1px solid var(--line);border-radius:11px;background:var(--surface);margin-bottom:8px;overflow:hidden;}
.sv details.week[open]{border-color:var(--line-strong);}
.sv details.week>summary{list-style:none;cursor:pointer;padding:12px 16px;display:grid;
  grid-template-columns:42px 92px 1fr auto;gap:14px;align-items:center;}
.sv details.week>summary::-webkit-details-marker{display:none;}
.sv details.week>summary:hover{background:var(--surface-2);}
.sv summary .wk{font-family:var(--font-mono);font-weight:700;font-size:15px;}
.sv summary .wk small{display:block;font-size:10px;color:var(--faint);font-weight:500;}
.sv summary .dt{font-family:var(--font-mono);font-size:12px;color:var(--muted);}
.sv summary .keys{font-size:13.5px;}
.sv summary .keys .mut{color:var(--muted);}
.sv summary .vol{text-align:right;font-family:var(--font-mono);}
.sv summary .vol .n{font-weight:700;font-size:15px;}
.sv summary .vol .n b{color:var(--accent-ink);}
.sv summary .vol small{display:block;font-size:10.5px;color:var(--faint);}
@media (max-width:820px){.sv details.week>summary{grid-template-columns:38px 1fr auto;}.sv summary .dt{display:none;}}
.sv .down-chip{color:var(--warn);border:1px solid var(--warn);border-radius:20px;font-size:10px;padding:0 7px;
  text-transform:uppercase;letter-spacing:.05em;}
.sv .gate-chip{color:var(--accent-ink);border:1px solid var(--accent);border-radius:20px;font-size:10px;font-weight:700;padding:0 7px;}
.sv .days{border-top:1px solid var(--line);padding:4px 16px 12px;}
.sv .day{display:grid;grid-template-columns:44px 80px 50px 1fr auto;gap:12px;align-items:center;padding:8px 0;
  border-bottom:1px solid var(--line);}
.sv .day:last-child{border-bottom:0;}
.sv .day .dow{font-family:var(--font-mono);font-size:12px;color:var(--muted);font-weight:600;}
.sv .day .dist{font-family:var(--font-mono);font-weight:700;font-size:13.5px;text-align:right;}
.sv .day .dist.rest{color:var(--faint);font-weight:500;}
.sv .day .desc{font-size:13.5px;}
.sv .day .tags{display:flex;gap:6px;justify-content:flex-end;flex-wrap:wrap;align-items:center;}
.sv .tag{font-size:10.5px;font-weight:600;padding:1px 6px;border-radius:5px;white-space:nowrap;
  border:1px solid var(--line-strong);color:var(--muted);}
.sv .tag.str{color:var(--pA);border-color:color-mix(in srgb,var(--pA) 45%,var(--line));}
.sv .tag.mp{color:var(--pB);border-color:color-mix(in srgb,var(--pB) 45%,var(--line));}
.sv .tag.act{color:var(--good);border-color:color-mix(in srgb,var(--good) 50%,var(--line));}
.sv .sdot{width:9px;height:9px;border-radius:50%;flex:0 0 auto;}
@media (max-width:820px){.sv .day{grid-template-columns:40px 46px 1fr;}.sv .day .type-chip,.sv .day .tags{display:none;}}
.sv .t-rest{background:transparent;color:var(--faint);border:1px dashed var(--line-strong);}
.sv .t-recovery{background:color-mix(in srgb,var(--pA) 14%,transparent);color:var(--pA);}
.sv .t-easy{background:var(--surface-2);color:var(--muted);border:1px solid var(--line);}
.sv .t-long{background:var(--accent-soft);color:var(--accent-ink);}
.sv .t-quality{background:color-mix(in srgb,var(--pC) 16%,transparent);color:var(--pC);}
.sv .t-race{background:var(--accent);color:#fff;}
.sv .wsum{display:flex;gap:16px;flex-wrap:wrap;padding:10px 16px 2px;font-size:12.5px;color:var(--muted);}
.sv .wsum b{color:var(--ink);font-family:var(--font-mono);}
.sv .wsum .flag{font-weight:600;}
.sv .banner{padding:.7rem 1rem;border-radius:12px;background:var(--accent-soft);
  border-left:4px solid var(--accent);font-size:13.5px;margin:4px 0 14px;}
.sv .t-tbd{background:color-mix(in srgb,var(--pD) 16%,transparent);color:var(--pD);}
.sv .trip-day{display:grid;grid-template-columns:44px 78px 108px 1fr;gap:12px;padding:9px 0;
  border-bottom:1px solid var(--line);align-items:baseline;}
.sv .trip-day:last-child{border-bottom:0;}
.sv .trip-day .dow{font-family:var(--font-mono);font-size:12px;color:var(--muted);font-weight:600;}
.sv .trip-day .dt{font-family:var(--font-mono);font-size:12px;color:var(--muted);}
.sv .trip-day .ttl{font-size:13.5px;}
.sv .trip-day .ttl b{font-weight:650;}
.sv .trip-day .ttl .dtl{display:block;color:var(--muted);font-size:12.5px;margin-top:2px;}
@media (max-width:820px){.sv .trip-day{grid-template-columns:38px 1fr;}.sv .trip-day .dt,.sv .trip-day .chip{display:none;}}
</style>"""

TRIP_TAG = {"travel": ("Travel", "t-rest"), "city": ("Sightseeing", "t-recovery"),
            "snow": ("Snowboarding", "t-quality"), "tourist": ("Flexible", "t-tbd"),
            "rest": ("Rest", "t-easy"), "race": ("Race", "t-race")}

PHASE_COLORS = ["var(--pA)", "var(--pB)", "var(--pC)", "var(--pD)", "var(--accent)"]


def load_json(name, default=None):
    p = os.path.join(DATA, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else default


def push_secrets_to_env():
    for k in ("STRAVA_CLIENT_ID", "STRAVA_CLIENT_SECRET", "STRAVA_REFRESH_TOKEN",
              "STRAVA_REFRESH_TOKEN_CAV", "STRAVA_REFRESH_TOKEN_JAMIE"):
        if k in st.secrets:
            os.environ[k] = str(st.secrets[k])


def refresh_runner(runner_id):
    push_secrets_to_env()
    from sync.run_sync import sync_runner
    return sync_runner(runner_id, write=True)


def esc(s):
    return html.escape(str(s))


# ---------------- HTML builders (Stevie style) ----------------

def facts_html(plan, wk_rows):
    m = plan["meta"]
    race = datetime.fromisoformat(m["race"]).date()
    start = datetime.fromisoformat(m["start"]).date()
    days_to_go = (race - date.today()).days
    longest = max((d["target_km"] for wk in plan["weeks"] for d in wk["days"]), default=0)
    ndays = sum(1 for d in plan["weeks"][max(len(plan["weeks"]) // 2, 0)]["days"] if d["type"] != "rest")
    logged = sum(w.get("actual_km", 0) for w in wk_rows.values())
    cells = [
        ("Goal", f'{esc(m["goal"])} <small>{esc(m["mp_per_km"])} /km</small>'),
        ("Race day", f'{race.strftime("%a %d %b")} <small>{days_to_go} days to go</small>'),
        ("Plan starts", f'{start.strftime("%a %d %b")} <small>{start.year}</small>'),
        ("Duration", f'{m["total_weeks"]} <small>weeks · {ndays} days/wk</small>'),
        ("Peak volume", f'{m["peak_km"]} <small>km/wk</small>'),
        ("Longest run", f'{longest:g} <small>km</small>'),
        ("Km logged", f'{logged:.0f} <small>since start</small>'),
    ]
    inner = "".join(f'<div class="fact"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in cells)
    return (f'<div class="eyebrow">Tokyo Marathon 2027 · Team dashboard</div>'
            f'<h2 style="font-size:26px;margin:6px 0 2px">{esc(m["name"])} — {esc(m["goal"])}</h2>'
            f'<p class="sub">{esc(m.get("goal_note",""))}</p>'
            f'<div class="facts">{inner}</div>')


def section(title, sub, body):
    return (f'<div class="sec"><div class="sec-head"><h2>{esc(title)}</h2>'
            f'{f"<p class=sub>{esc(sub)}</p>" if sub else ""}</div>{body}</div>')


def approach_html(plan):
    phases = []
    for wk in plan["weeks"]:
        if not phases or phases[-1][0] != wk["phase"]:
            phases.append([wk["phase"], wk["week"], wk["week"]])
        else:
            phases[-1][2] = wk["week"]
    plist = "".join(f'<li><b>{esc(p)}</b> <span class="mut">Wk {a}–{b}</span></li>' for p, a, b in phases)
    c = plan.get("content", {})
    cp = c.get("checkpoints", {}).get("intro", "")
    sc = c.get("strength", {}).get("intro", "")
    return ('<div class="grid3">'
            f'<div class="card"><h3>Phases</h3><ul class="tight">{plist}</ul></div>'
            f'<div class="card"><h3>Strength &amp; life</h3><p>{esc(sc)}</p></div>'
            f'<div class="card"><h3>Checkpoints</h3><p>{esc(cp)}</p></div>'
            '</div>')


def paces_html(plan):
    c = plan.get("content", {})
    p = c.get("paces", {})
    dots = ["var(--pA)", "var(--muted)", "var(--accent-ink)", "var(--accent-ink)",
            "var(--pC)", "var(--pB)", "var(--pD)", "var(--faint)"]
    rows = ""
    for i, r in enumerate(p.get("rows", [])):
        dot = dots[i % len(dots)]
        rows += (f'<tr><td><span class="zone-dot" style="background:{dot}"></span>{esc(r[0])}</td>'
                 f'<td class="num">{esc(r[1])}</td><td class="num">{esc(r[2])}</td></tr>')
    note = f'<p class="sub" style="margin-top:10px">{esc(p["note"])}</p>' if p.get("note") else ""
    tbl = (f'<table class="data"><tr><th>Zone</th><th class="num">/km</th><th class="num">/mile</th></tr>{rows}</table>'
           f'{note}')
    # weekly structure template from a representative peak week
    peak = max(plan["weeks"], key=lambda w: w["target_km"])
    rowt = ""
    for d in peak["days"]:
        rowt += f'<div class="row"><div class="d">{esc(d["dow"])}</div><div class="s">{esc(d["session"])}</div></div>'
    tmpl = f'<h3>Weekly shape · Wk {peak["week"]} (peak)</h3><div class="tmpl">{rowt}</div>'
    goals = ""
    if c.get("goals"):
        g = c["goals"]
        gr = "".join("<tr>" + "".join(f'<td class="num">{esc(x)}</td>' if i else f"<td>{esc(x)}</td>"
                     for i, x in enumerate(row)) + "</tr>" for row in g["rows"])
        gh = "".join(f'<th class="num">{esc(h)}</th>' if i else f"<th>{esc(h)}</th>" for i, h in enumerate(g["headers"]))
        goals = f'<div class="card" style="margin-top:16px"><h3>Your goals</h3><table class="data"><tr>{gh}</tr>{gr}</table></div>'
    return f'<div class="grid2"><div class="card">{tbl}</div><div class="card">{tmpl}</div></div>{goals}'


def gates_html(plan):
    cp = plan.get("content", {}).get("checkpoints", {})
    rows = cp.get("rows", [])
    intro = f'<p class="banner">{esc(cp["intro"])}</p>' if cp.get("intro") else ""
    cards = ""
    for i, r in enumerate(rows):
        wkdate = r[0]
        test = r[1]
        target = r[-1]
        decisive = "half" in test.lower() or "half" in wkdate.lower()
        wk = wkdate.split("·")[0].strip() if "·" in wkdate else wkdate
        dt = wkdate.split("·", 1)[1].strip() if "·" in wkdate else ""
        badge = '<span class="badge-dec">Decisive</span>' if decisive else ""
        cards += (f'<div class="gate{" decisive" if decisive else ""}">'
                  f'<div class="id">G{i}<small>{esc(wk)}</small></div>'
                  f'<div><div class="what">{esc(test)}{badge}</div>'
                  f'<div class="blurb">{esc(dt)}</div></div>'
                  f'<div class="target">{esc(target)}</div></div>')
    notes = "".join(f"<li>{esc(n)}</li>" for n in cp.get("notes", []))
    notes = f'<ul class="tight" style="margin-top:14px">{notes}</ul>' if notes else ""
    return f'{intro}<div class="gates">{cards}</div>{notes}'


def day_html(d, pd_, today_iso):
    typ = d["type"]
    cls = TYPE_CLASS.get(typ, "t-easy")
    label = TYPE_LABEL.get(typ, typ.title())
    dist = "—" if d["type"] == "rest" or not d["target_km"] else f'{d["target_km"]:g}k'
    distcls = "dist rest" if dist == "—" else "dist"
    # progress overlay
    status = pd_.get("status")
    dot = ""
    if status in STATUS_COLOR:
        dot = f'<span class="sdot" style="background:{STATUS_COLOR[status]}" title="{status}"></span>'
    tags = ""
    sess = d["session"]
    if "S&C A" in sess:
        tags += '<span class="tag str">Str A</span>'
    if "S&C B" in sess:
        tags += '<span class="tag str">Str B</span>'
    if "@ MP" in sess and "no MP" not in sess:
        tags += '<span class="tag mp">MP</span>'
    actual, pace = pd_.get("actual_km", 0), pd_.get("pace_str")
    if actual:
        tags += f'<span class="tag act">✓ {actual:.1f}k{(" · " + pace) if pace else ""}</span>'
    return (f'<div class="day"><span class="dow">{esc(d["dow"])}</span>'
            f'<span class="chip type-chip {cls}">{esc(label)}</span>'
            f'<span class="{distcls}">{dist}</span>'
            f'<span class="desc">{esc(sess)}</span>'
            f'<span class="tags">{dot}{tags}</span></div>')


def weeks_html(plan, progress, cur):
    wk_rows = progress.get("weeks", {})
    days_map = progress.get("days", {})
    today_iso = date.today().isoformat()
    # phase groups
    groups = []
    for wk in plan["weeks"]:
        if not groups or groups[-1]["phase"] != wk["phase"]:
            groups.append({"phase": wk["phase"], "weeks": []})
        groups[-1]["weeks"].append(wk)
    out = ""
    for gi, g in enumerate(groups):
        color = PHASE_COLORS[gi % len(PHASE_COLORS)]
        a, b = g["weeks"][0]["week"], g["weeks"][-1]["week"]
        out += (f'<div class="phase-group"><div class="phase-bar">'
                f'<span class="phase-tag" style="background:{color}">{chr(65+gi)}</span>'
                f'<h3>{esc(g["phase"])}</h3><span class="rng">Wk {a}–{b}</span></div>')
        for wk in g["weeks"]:
            w = wk["week"]
            start = datetime.fromisoformat(wk["start"]).date()
            end = start + pd.Timedelta(days=6)
            # summary keys: pull the quality/long headline
            quality = next((d["session"] for d in wk["days"] if d["type"] in ("quality", "tt")), "")
            longrun = next((d for d in wk["days"] if d["type"] in ("long", "race")), None)
            lr = f'LR {longrun["target_km"]:g}k' if longrun else ""
            keys = esc(quality.split("  +")[0][:44]) if quality else '<span class="mut">easy week</span>'
            chips = ""
            foc = wk.get("focus", "")
            if "Cut-back" in foc or "recovery" in foc.lower():
                chips += '<span class="down-chip">down</span>'
            if "checkpoint" in foc.lower() or "tune-up" in foc.lower() or "RACE" in foc:
                chips += f'<span class="gate-chip">{esc(foc.split("(")[0][:16])}</span>'
            summary = (f'<summary><div class="wk">{w}<small>WK</small></div>'
                       f'<div class="dt">{start.strftime("%d %b")}<br>{end.strftime("%d %b")}</div>'
                       f'<div class="keys">{keys} <span class="mut">·</span> '
                       f'<span class="mut">{esc(lr)}</span> {chips}</div>'
                       f'<div class="vol"><div class="n"><b>{wk["target_km"]}k</b></div><small>volume</small></div></summary>')
            # per-week progress summary line
            wsum = wk_rows.get(str(w), {})
            wline = ""
            if wsum:
                flag = wsum.get("flag", "")
                fcolor = "var(--good)" if flag.startswith("✓") else "var(--warn)"
                wline = (f'<div class="wsum"><span>Planned <b>{wsum["planned_km"]:.0f}k</b></span>'
                         f'<span>Actual <b>{wsum["actual_km"]:.0f}k</b></span>'
                         f'<span>Quality <b>{wsum["quality_hit"]}/{wsum["quality_planned"]}</b></span>'
                         f'<span>Done <b>{wsum["done"]}</b></span>'
                         f'{f"<span class=flag style=color:{fcolor}>{esc(flag)}</span>" if flag else ""}</div>')
            days = "".join(day_html(d, days_map.get(d["date"], {}), today_iso) for d in wk["days"])
            openattr = " open" if w == cur else ""
            out += f'<details class="week"{openattr}>{summary}{wline}<div class="days">{days}</div></details>'
        out += "</div>"
    return out


def ref_table(headers, rows):
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table class="data"><tr>{th}</tr>{tr}</table>'


def strength_html(plan):
    sc = plan.get("content", {}).get("strength", {})
    if not sc:
        return ""
    body = f'<p class="sub" style="margin-bottom:12px">{esc(sc.get("intro",""))}</p>'
    for blk in sc.get("blocks", []):
        note = f'<p class="sub" style="margin-bottom:10px">{esc(blk["note"])}</p>' if blk.get("note") else ""
        body += (f'<div class="card" style="margin-bottom:14px"><h3>{esc(blk["title"])}</h3>'
                 f'{note}{ref_table(blk["headers"], blk["rows"])}</div>')
    return body


def fuel_html(plan):
    fu = plan.get("content", {}).get("fuel", {})
    if not fu:
        return ""
    body = f'<p class="sub" style="margin-bottom:12px">{esc(fu.get("intro",""))}</p>'
    for sec in fu.get("sections", []):
        body += (f'<div class="card" style="margin-bottom:14px"><h3>{esc(sec["title"])}</h3>'
                 f'{ref_table(sec["headers"], sec["rows"])}</div>')
    return body


def research_html(plan):
    rs = plan.get("content", {}).get("research", {})
    if not rs:
        return ""
    intro = f'<p class="sub" style="margin-bottom:12px">{esc(rs.get("intro",""))}</p>'
    cards = ""
    for sec in rs.get("sections", []):
        cards += (f'<div class="card" style="margin-bottom:12px"><h3>{esc(sec["title"])}</h3>'
                  f'<p>{esc(sec["detail"])}</p></div>')
    return intro + cards


def tips_html(plan):
    tips = plan.get("content", {}).get("tips", [])
    lis = "".join(f'<li><b>{esc(t[0])}</b> — {esc(t[1])}</li>' for t in tips)
    return f'<div class="card"><ul class="tight">{lis}</ul></div>'


def trip_facts_html(trip):
    m = trip["meta"]
    start = datetime.fromisoformat(m["start"]).date()
    end = datetime.fromisoformat(m["end"]).date()
    race = date(2027, 3, 7)
    cells = [
        ("Depart", start.strftime("%a %d %b")),
        ("Return home", end.strftime("%a %d %b")),
        ("Trip length", f'{(end-start).days + 1} <small>days</small>'),
        ("Race day", f'{race.strftime("%a %d %b")} <small>Tokyo Marathon</small>'),
    ]
    inner = "".join(f'<div class="fact"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in cells)
    return (f'<div class="eyebrow">{esc(m["title"])}</div>'
            f'<h2 style="font-size:26px;margin:6px 0 2px">Kyoto → Tokyo Marathon → Niseko → Sapporo</h2>'
            f'<p class="sub">{esc(m.get("note",""))}</p><div class="facts">{inner}</div>')


def trip_legs_html(trip):
    out = ""
    for i, leg in enumerate(trip["legs"]):
        color = PHASE_COLORS[i % len(PHASE_COLORS)]
        blurb = f'<p class="sub" style="margin:2px 0 8px">{esc(leg["blurb"])}</p>' if leg.get("blurb") else ""
        rows = ""
        for dd in leg["days"]:
            dt = datetime.fromisoformat(dd["date"]).date()
            label, cls = TRIP_TAG.get(dd["tag"], ("Flexible", "t-tbd"))
            rows += (f'<div class="trip-day"><span class="dow">{dt.strftime("%a")}</span>'
                     f'<span class="dt">{dt.strftime("%d %b")}</span>'
                     f'<span class="chip {cls}">{esc(label)}</span>'
                     f'<span class="ttl"><b>{esc(dd["title"])}</b><span class="dtl">{esc(dd["detail"])}</span></span></div>')
        out += (f'<div class="phase-group"><div class="phase-bar">'
                f'<span class="phase-tag" style="background:{color}">{chr(65+i)}</span>'
                f'<h3>{esc(leg["name"])}</h3></div>{blurb}<div class="days">{rows}</div></div>')
    return out


def render_trip(trip):
    st.markdown(STYLE + '<div class="sv">' + trip_facts_html(trip) +
                section("Itinerary", "Open to edit the plan — the 14–20 Mar block is still a placeholder.",
                        trip_legs_html(trip)) + '</div>', unsafe_allow_html=True)


LEGEND = ('<div class="legend">'
          '<span><i class="chip t-easy" style="width:22px">&nbsp;</i> Easy / recovery</span>'
          '<span><i class="chip t-long" style="width:22px">&nbsp;</i> Long run</span>'
          '<span><i class="chip t-quality" style="width:22px">&nbsp;</i> Quality</span>'
          '<span><i class="chip t-race" style="width:22px">&nbsp;</i> Race</span>'
          '<span><span class="sdot" style="background:var(--good)"></span> done '
          '<span class="sdot" style="background:var(--warn)"></span> partial '
          '<span class="sdot" style="background:var(--accent)"></span> missed</span></div>')


def render_runner(runner_id):
    plan = load_json(f"plan_{runner_id}.json")
    if not plan:
        st.error(f"No plan for {runner_id} — run plan/plan_generator.py."); return
    progress = load_json(f"progress_{runner_id}.json",
                         {"days": {}, "weeks": {}, "last_sync": None, "tracker": None})
    wk_rows = progress.get("weeks", {})
    content = plan.get("content", {})
    today = date.today()
    cur = next((wk["week"] for wk in plan["weeks"]
                if datetime.fromisoformat(wk["start"]).date() <= today
                <= datetime.fromisoformat(wk["start"]).date() + pd.Timedelta(days=6)), 1)

    # Strava control row (native Streamlit)
    a, b = st.columns([3, 1])
    a.caption(f"Last Strava sync: {progress.get('last_sync') or 'never — connect Strava or hit refresh'}")
    if b.button("🔄 Refresh from Strava", key=f"r_{runner_id}", use_container_width=True):
        try:
            with st.spinner("Pulling from Strava…"):
                res = refresh_runner(runner_id)
            st.warning("No Strava creds for this runner (see README).") if res is None else (st.success("Synced!"), st.rerun())
        except Exception as e:
            st.error(f"Sync failed: {e}")

    # ---- hero (facts strip) stays fixed above the subtabs ----
    banner = f'<div class="banner">{esc(content["banner"])}</div>' if content.get("banner") else ""
    st.markdown(STYLE + '<div class="sv">' + banner + facts_html(plan, wk_rows) + "</div>", unsafe_allow_html=True)

    # ---- everything else lives in subtabs ----
    sub = st.tabs(["📋 Plan", "🧭 Approach", "🎯 Paces", "🚦 Gates", "📈 Volume",
                   "💪 Strength", "🥗 Fuel & life", "💡 Tips", "🔬 Research"])

    with sub[0]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("The 33-week plan", "Grouped by phase — open any week for the day-by-day.",
                            LEGEND + weeks_html(plan, progress, cur)) + "</div>", unsafe_allow_html=True)
    with sub[1]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("The approach", "Why the plan is shaped the way it is.", approach_html(plan))
                    + "</div>", unsafe_allow_html=True)
    with sub[2]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("Pace zones", f'Anchored on {plan["meta"]["goal"]} (MP {plan["meta"]["mp_per_km"]}/km).',
                            paces_html(plan)) + "</div>", unsafe_allow_html=True)
    with sub[3]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("Decision gates", "Checkpoints that confirm the plan is on track.", gates_html(plan))
                    + "</div>", unsafe_allow_html=True)
    with sub[4]:
        st.markdown(STYLE + '<div class="sv"><div class="sec"><div class="sec-head"><h2>Weekly volume</h2>'
                    '<p class="sub">Planned vs actual (Strava).</p></div></div></div>', unsafe_allow_html=True)
        if wk_rows:
            rows = [{"Week": wk["week"], "Planned": wk["target_km"],
                     "Actual": wk_rows.get(str(wk["week"]), {}).get("actual_km", 0)} for wk in plan["weeks"]]
            st.bar_chart(pd.DataFrame(rows).set_index("Week"), color=["#c7d2e0", "#2f8f7e"], height=200)
        else:
            st.caption("No synced weeks yet.")
    with sub[5]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("Strength &amp; conditioning", "", strength_html(plan)) + "</div>", unsafe_allow_html=True)
    with sub[6]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("Fuel &amp; life", "", fuel_html(plan)) + "</div>", unsafe_allow_html=True)
    with sub[7]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("Tips", "", tips_html(plan)) + "</div>", unsafe_allow_html=True)
    with sub[8]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("Research &amp; rationale", "Why the plan is shaped this way, and what we've looked at.",
                            research_html(plan)) + "</div>", unsafe_allow_html=True)


# ---------------- page ----------------
st.title("🏃 Tokyo Marathon 2027 — Team dashboard")
runners = load_json("runners.json", [])
trip = load_json("trip.json")
if not runners:
    st.error("No runners.json — run: python plan/plan_generator.py")
else:
    labels = [f'{r["name"]} · {r["goal"]}' for r in runners] + (["🗾 Trip"] if trip else [])
    top_tabs = st.tabs(labels)
    for tab, r in zip(top_tabs, runners):
        with tab:
            render_runner(r["id"])
    if trip:
        with top_tabs[len(runners)]:
            render_trip(trip)
st.divider()
st.caption("Adjustments are suggestions — you decide. Data © each runner, via Strava (personal use). "
           "Auto-syncs a few times a day; hit refresh for on-demand. Design adapted from Stevie's Sub-3:15 build.")
