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

/* ---- glam: progress rings, tier/streak badges, celebratory pills ---- */
.sv{--glam-grad:linear-gradient(135deg,var(--accent),#ff9a56);
    --glam-gold:linear-gradient(135deg,#ffe29a,#ffb347);
    --glam-glow:0 0 22px rgba(255,140,66,.4);}
.sv .glam-row{display:flex;gap:14px;flex-wrap:wrap;align-items:stretch;margin:12px 0 4px;}
.sv .ring-card{flex:1 1 180px;display:flex;align-items:center;gap:14px;padding:14px 18px;
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);}
.sv .ring{--pct:0;--ring-color:var(--accent);width:76px;height:76px;border-radius:50%;flex:0 0 auto;
  display:grid;place-items:center;position:relative;
  background:conic-gradient(var(--ring-color) calc(var(--pct)*1%), var(--line) 0);
  animation:ringFade .7s ease both;}
.sv .ring::before{content:"";position:absolute;inset:7px;border-radius:50%;background:var(--surface);}
.sv .ring-val{position:relative;z-index:1;font-family:var(--font-mono);font-weight:800;font-size:16px;line-height:1;}
.sv .ring-txt{display:flex;flex-direction:column;gap:2px;}
.sv .ring-title{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:700;}
.sv .ring-cap{font-size:12.5px;color:var(--muted);}
.sv .tier-badge{display:inline-block;margin-top:2px;padding:2px 11px;border-radius:999px;font-size:10.5px;
  font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:var(--glam-grad);
  box-shadow:0 2px 10px rgba(255,140,66,.35);width:fit-content;}
.sv .streak-card{flex:1 1 180px;display:flex;align-items:center;gap:12px;padding:14px 18px;
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);}
.sv .streak-badge{display:inline-flex;align-items:center;gap:6px;padding:6px 16px;border-radius:999px;
  font-weight:800;font-size:15px;background:var(--glam-gold);color:#3d2a00;box-shadow:0 2px 14px rgba(255,179,71,.45);
  animation:ringFade .7s ease both;}
.sv .streak-sub{font-size:12.5px;color:var(--muted);}
@keyframes ringFade{from{opacity:0;transform:scale(.85);}to{opacity:1;transform:scale(1);}}
@keyframes popIn{from{transform:scale(.7);opacity:0;}to{transform:scale(1);opacity:1;}}
@keyframes glowPulse{0%,100%{box-shadow:0 0 0 rgba(47,143,126,0);}50%{box-shadow:0 0 12px rgba(47,143,126,.45);}}
.sv .tag.act{background:linear-gradient(135deg,color-mix(in srgb,var(--good) 80%,white 20%),var(--good));
  color:#fff;border:none;animation:popIn .35s ease both, glowPulse 2.6s ease-in-out infinite;}
.sv .crushed-chip{display:inline-flex;align-items:center;gap:4px;padding:2px 10px;border-radius:999px;
  font-size:10px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:#3d2a00;
  background:var(--glam-gold);box-shadow:0 2px 10px rgba(255,179,71,.45);animation:popIn .4s ease both;}
@media (max-width:820px){.sv .glam-row{flex-direction:column;}}
.sv .celebrate{display:flex;align-items:center;gap:14px;padding:14px 20px;border-radius:var(--radius);
  background:linear-gradient(135deg,var(--accent),#ff9a56);color:#fff;margin:4px 0 14px;
  box-shadow:var(--glam-glow);animation:celebrateIn .5s cubic-bezier(.22,1,.36,1) both;}
.sv .celebrate .ce-emoji{font-size:30px;line-height:1;animation:bounce 1.6s ease-in-out infinite;}
.sv .celebrate .ce-title{font-weight:800;font-size:16px;}
.sv .celebrate .ce-sub{font-size:13px;opacity:.9;margin-top:2px;}
@keyframes celebrateIn{from{opacity:0;transform:translateY(-8px) scale(.97);}to{opacity:1;transform:translateY(0) scale(1);}}
@keyframes bounce{0%,100%{transform:translateY(0);}50%{transform:translateY(-4px);}}
.sv .celebrate.todo{background:linear-gradient(135deg,var(--pA),var(--pB));}

/* ---- analytics ---- */
.sv .stat-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;margin-bottom:16px;}
.sv .stat{background:var(--surface);padding:13px 16px;}
.sv .stat .k{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);}
.sv .stat .v{font-size:19px;font-weight:700;margin-top:3px;font-family:var(--font-mono);}
.sv .predict-card{display:flex;align-items:center;gap:20px;padding:20px 22px;background:var(--surface);
  border:1px solid var(--line);border-radius:var(--radius);flex-wrap:wrap;}
.sv .predict-time{font-family:var(--font-mono);font-weight:800;font-size:34px;color:var(--accent-ink);line-height:1;}
.sv .predict-meta{color:var(--muted);font-size:12.5px;}
.sv .acwr-band{position:relative;height:10px;border-radius:999px;background:linear-gradient(90deg,
  var(--pC) 0%, var(--good) 32%, var(--good) 56%, var(--pC) 78%, var(--accent) 100%);margin:10px 0 4px;}
.sv .acwr-marker{position:absolute;top:-4px;width:3px;height:18px;background:var(--ink);border-radius:2px;
  transform:translateX(-50%);}
.sv .heatmap-wrap{overflow-x:auto;padding-bottom:8px;}
.sv .heatmap{display:grid;grid-auto-flow:column;grid-template-rows:repeat(7,13px);gap:3px;width:max-content;}
.sv .hc{width:13px;height:13px;border-radius:3px;background:var(--line);}
.sv .heatmap-legend{display:flex;align-items:center;gap:5px;margin-top:8px;font-size:11px;color:var(--muted);}
.sv .heatmap-legend .hc{width:11px;height:11px;}
@media (max-width:820px){.sv .stat-row{grid-template-columns:repeat(2,1fr);}}
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

TIERS = [(90, "Legend"), (75, "Elite"), (55, "Grinding"), (35, "Building"), (15, "Rookie"), (0, "Just started")]


def tier_for(pct):
    for min_p, label in TIERS:
        if pct >= min_p:
            return label
    return "Just started"


def ring_html(pct, big, title, caption, color="var(--accent)"):
    pct = max(0, min(100, round(pct)))
    return (f'<div class="ring-card"><div class="ring" style="--pct:{pct};--ring-color:{color}">'
            f'<div class="ring-val">{pct}%</div></div>'
            f'<div class="ring-txt"><div class="ring-title">{esc(title)}</div>'
            f'<div class="ring-cap">{esc(caption)}</div>'
            f'<div class="tier-badge">{esc(big)}</div></div></div>')


def compute_streak(plan, wk_rows):
    """Consecutive on-track weeks ending at the most recent week that's actually started."""
    streak = 0
    started = False
    for wk in sorted(plan["weeks"], key=lambda w: -w["week"]):
        w = wk_rows.get(str(wk["week"]))
        if not w or w.get("planned_km_due", 0) <= 0:
            continue
        started = True
        if w.get("flag", "").startswith("✓"):
            streak += 1
        else:
            break
    return streak if started else 0


def glam_row_html(plan, progress, cur):
    wk_rows = progress.get("weeks", {})
    cur_w = wk_rows.get(str(cur), {})
    # Ring tracks progress toward the FULL week's target so it fills up gradually across
    # the week (day 2 of 7 isn't "100% done") — the under/over-target text flag elsewhere
    # still judges against km due so far, which is the right comparison for that message.
    planned = cur_w.get("planned_km", 0)
    week_pct = (cur_w.get("actual_km", 0) / planned * 100) if planned > 0 else 0
    week_ring = ring_html(week_pct, tier_for(week_pct), "This week",
                           f'{cur_w.get("actual_km",0):.0f} of {planned:.0f} km this week', "var(--good)")

    done_total = sum(w["done"] for w in wk_rows.values())
    due_total = sum(w["done"] + w["partial"] + w["missed"] for w in wk_rows.values())
    consist_pct = (done_total / due_total * 100) if due_total > 0 else 0
    consist_ring = ring_html(consist_pct, tier_for(consist_pct), "Consistency",
                              f'{done_total} of {due_total} sessions done', "var(--accent)")

    streak = compute_streak(plan, wk_rows)
    streak_html = ""
    if streak > 0:
        streak_html = (f'<div class="streak-card"><span class="streak-badge">🔥 {streak}</span>'
                        f'<span class="streak-sub">week{"s" if streak != 1 else ""} on track in a row</span></div>')
    return f'<div class="glam-row">{week_ring}{consist_ring}{streak_html}</div>'


def _format_duration(secs):
    if not secs:
        return None
    secs = int(secs)
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def celebration_html(plan, progress):
    """Today's status: a call-to-action if the run's still to do, a dopamine hit with
    stats once it's logged. Silent on rest days."""
    today_iso = date.today().isoformat()
    d = progress.get("days", {}).get(today_iso)
    if not d or d.get("type") == "rest":
        return ""
    status = d.get("status")
    sess = d.get("session", "today's run")
    target = d.get("target_km", 0)
    if status in ("Done", "Partial"):
        acts = d.get("activities") or []
        lead = max(acts, key=lambda a: a.get("distance_km", 0)) if acts else {}
        actual, pace = d.get("actual_km", 0), d.get("pace_str")
        dur = _format_duration(lead.get("moving_time_s"))
        hr, elev = lead.get("avg_hr"), lead.get("elev_gain_m")
        stats = [f'{actual:.1f} km']
        if pace: stats.append(f'{pace}/km')
        if dur: stats.append(dur)
        if hr: stats.append(f'{round(hr)} bpm avg')
        if elev: stats.append(f'{round(elev)} m elev')
        if status == "Done":
            title, emoji, cls = "Nice work — today's session is done! 🎉", "🏅", "celebrate"
        else:
            title, emoji, cls = "Good start today — a bit more would seal it 💪", "⏱️", "celebrate"
        sub = f'{sess} — ' + " · ".join(stats)
    elif status == "Upcoming":
        title, emoji, cls = "Today's session", "🎯", "celebrate todo"
        sub = sess + (f' — {target:g} km planned' if target else '')
    else:
        return ""
    return (f'<div class="{cls}"><span class="ce-emoji">{emoji}</span>'
            f'<div><div class="ce-title">{esc(title)}</div><div class="ce-sub">{esc(sub)}</div></div></div>')


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
            wsum_peek = wk_rows.get(str(w), {})
            total_sessions = wsum_peek.get("done", 0) + wsum_peek.get("partial", 0) + wsum_peek.get("missed", 0)
            if (total_sessions and wsum_peek.get("missed", 0) == 0 and wsum_peek.get("partial", 0) == 0
                    and wsum_peek.get("actual_km", 0) >= 0.95 * wsum_peek.get("planned_km", 1)):
                chips += '<span class="crushed-chip">🏆 Crushed</span>'
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


def diet_html(plan):
    d = plan.get("content", {}).get("diet", {})
    if not d:
        return ""
    body = f'<p class="sub" style="margin-bottom:12px">{esc(d.get("intro",""))}</p>'
    if d.get("targets"):
        body += f'<div class="card" style="margin-bottom:14px"><h3>Targets</h3>{ref_table(d["targets"]["headers"], d["targets"]["rows"])}</div>'
    if d.get("smoothie"):
        sm = d["smoothie"]
        ing = "".join(f"<li>{esc(i)}</li>" for i in sm.get("ingredients", []))
        body += (f'<div class="card" style="margin-bottom:14px"><h3>{esc(sm["title"])}</h3>'
                 f'<ul class="tight">{ing}</ul>'
                 f'<p class="sub" style="margin-top:10px">{esc(sm.get("note",""))}</p></div>')
    if d.get("additions"):
        body += f'<div class="card" style="margin-bottom:14px"><h3>Recommended add-ins</h3>{ref_table(d["additions"]["headers"], d["additions"]["rows"])}</div>'
    if d.get("meals"):
        body += f'<div class="card" style="margin-bottom:14px"><h3>Meals by time of day</h3>{ref_table(d["meals"]["headers"], d["meals"]["rows"])}</div>'
    notes = "".join(f"<li>{esc(n)}</li>" for n in d.get("notes", []))
    if notes:
        body += f'<ul class="tight">{notes}</ul>'
    return body


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


# ---------------- Analytics ----------------

def decode_polyline(encoded):
    """Google encoded-polyline decoder (Strava's summary_polyline format). No external dep."""
    if not encoded:
        return []
    points, index, lat, lng = [], 0, 0, 0
    n = len(encoded)
    while index < n:
        for is_lat in (True, False):
            shift, result = 0, 0
            while True:
                b = ord(encoded[index]) - 63
                index += 1
                result |= (b & 0x1f) << shift
                shift += 5
                if b < 0x20:
                    break
            d = ~(result >> 1) if (result & 1) else (result >> 1)
            if is_lat:
                lat += d
            else:
                lng += d
        points.append((lat / 1e5, lng / 1e5))
    return points


def gather_activities(progress):
    """Flatten every logged activity out of progress['days'], tagged with the plan day-type."""
    out = []
    for dt, d in progress.get("days", {}).items():
        for a in (d.get("activities") or []):
            if not a.get("distance_km"):
                continue
            out.append({**a, "date": dt, "day_type": d.get("type"), "session": d.get("session")})
    out.sort(key=lambda a: a["date"])
    return out


def _fmt_hms(secs):
    if not secs:
        return "—"
    secs = int(secs)
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def analytics_headline_html(acts):
    if not acts:
        return '<p class="sub">No runs logged yet — connect Strava and hit refresh.</p>'
    total_km = sum(a["distance_km"] for a in acts)
    total_s = sum(a.get("moving_time_s") or 0 for a in acts)
    total_elev = sum(a.get("elev_gain_m") or 0 for a in acts)
    hrs = [a["avg_hr"] for a in acts if a.get("avg_hr")]
    avg_hr = sum(hrs) / len(hrs) if hrs else None
    avg_pace = (total_s / 60.0) / total_km if total_km > 0 else None
    cells = [
        ("Runs logged", str(len(acts))),
        ("Total distance", f'{total_km:.0f} km'),
        ("Total time", _fmt_hms(total_s)),
        ("Total elevation", f'{total_elev:.0f} m'),
        ("Avg pace", _fmt_hms(avg_pace * 60) + "/km" if avg_pace else "—"),
        ("Avg HR", f'{avg_hr:.0f} bpm' if avg_hr else "—"),
    ]
    return '<div class="stat-row">' + "".join(
        f'<div class="stat"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div></div>' for k, v in cells
    ) + '</div>'


def pace_trend_df(acts):
    rows = []
    for a in acts:
        if not a.get("pace_min_km") or a.get("day_type") == "rest":
            continue
        bucket = "Long" if a["day_type"] in ("long", "race") else ("Quality" if a["day_type"] in ("quality", "tt") else "Easy")
        rows.append({"date": a["date"], "Pace (min/km)": a["pace_min_km"], "Type": bucket})
    if not rows:
        return None
    df = pd.DataFrame(rows)
    return df.pivot_table(index="date", columns="Type", values="Pace (min/km)", aggfunc="mean")


def hr_trend_df(acts):
    rows = [{"date": a["date"], "Avg HR": a["avg_hr"]} for a in acts if a.get("avg_hr")]
    if len(rows) < 3:
        return None
    df = pd.DataFrame(rows).groupby("date").mean()
    return df


def acwr_series(plan, progress):
    """Acute:chronic workload ratio — 7-day load vs the 28-day daily average x7, per day."""
    days = progress.get("days", {})
    all_dates = sorted(d["date"] for wk in plan["weeks"] for d in wk["days"] if d["date"] <= date.today().isoformat())
    if len(all_dates) < 8:
        return None, None
    load = {dt: days.get(dt, {}).get("actual_km", 0) for dt in all_dates}
    s = pd.Series(load).sort_index()
    s.index = pd.to_datetime(s.index)
    acute = s.rolling(7, min_periods=1).sum()
    chronic = s.rolling(28, min_periods=7).mean() * 7
    ratio = (acute / chronic).replace([float("inf")], None).dropna()
    if ratio.empty:
        return None, None
    return ratio, ratio.iloc[-1]


def acwr_band_html(current):
    pct = max(0, min(100, (current / 2.0) * 100))
    if current < 0.8:
        status, color = "Undertraining a little slack", "var(--pC)"
    elif current <= 1.3:
        status, color = "Sweet spot", "var(--good)"
    elif current <= 1.5:
        status, color = "Elevated — keep an eye on it", "var(--pC)"
    else:
        status, color = "High spike — injury-risk zone", "var(--accent)"
    return (f'<div class="acwr-band"><div class="acwr-marker" style="left:{pct}%"></div></div>'
            f'<p class="sub"><b style="color:{color}">{current:.2f}</b> · {esc(status)} '
            f'<span class="mut">(0.8–1.3 is the commonly-cited safe zone)</span></p>')


def predict_race_time(progress):
    days = progress.get("days", {})
    candidates = []
    for dt, d in days.items():
        if d.get("type") not in ("tt", "race") or d.get("status") not in ("Done", "Partial"):
            continue
        for a in (d.get("activities") or []):
            dist, t = a.get("distance_km"), a.get("moving_time_s")
            if dist and t and dist > 1:
                candidates.append({"date": dt, "session": d.get("session", ""), "distance_km": dist,
                                    "time_s": t, "predicted_marathon_s": t * (42.195 / dist) ** 1.06})
    if not candidates:
        return None
    return min(candidates, key=lambda c: c["predicted_marathon_s"])


def predict_html(pred, goal_note):
    if not pred:
        return ('<p class="sub">No time-trial or race results logged yet — a prediction appears here once you '
                'log a 5K/10K/half checkpoint or race. In the meantime, see the Gates tab for planned checkpoints.</p>')
    m_s = pred["predicted_marathon_s"]
    mp_pace = _fmt_hms((m_s / 42.195))
    return (f'<div class="predict-card"><div><div class="predict-time">{_fmt_hms(m_s)}</div>'
            f'<div class="predict-meta">Predicted marathon time (Riegel formula)</div></div>'
            f'<div class="predict-meta">From {pred["distance_km"]:.1f} km in {_fmt_hms(pred["time_s"])} '
            f'on {pred["date"]} — {esc(pred["session"][:60])}<br>Implied MP: {mp_pace}/km<br>'
            f'{esc(goal_note)}</div></div>')


def calendar_heatmap_html(plan, progress):
    days_map = progress.get("days", {})
    today_iso = date.today().isoformat()
    all_days = [d for wk in plan["weeks"] for d in wk["days"] if d["date"] <= today_iso]
    if not all_days:
        return '<p class="sub">Nothing logged yet.</p>'
    max_km = max((days_map.get(d["date"], {}).get("actual_km", 0) for d in all_days), default=0) or 1
    cells = ""
    for d in all_days:
        km = days_map.get(d["date"], {}).get("actual_km", 0)
        if d["type"] == "rest" and km <= 0:
            bg = "var(--line)"
        else:
            ratio = min(1, km / max_km) if km > 0 else 0
            bg = "var(--line)" if ratio == 0 else f"color-mix(in srgb, var(--good) {round(20+ratio*80)}%, var(--line))"
        title = f'{d["date"]} — {km:.1f} km' if km else f'{d["date"]} — rest/no run'
        cells += f'<div class="hc" style="background:{bg}" title="{esc(title)}"></div>'
    return (f'<div class="heatmap-wrap"><div class="heatmap">{cells}</div>'
            f'<div class="heatmap-legend">Less <span class="hc" style="background:var(--line)"></span>'
            f'<span class="hc" style="background:color-mix(in srgb, var(--good) 40%, var(--line))"></span>'
            f'<span class="hc" style="background:color-mix(in srgb, var(--good) 70%, var(--line))"></span>'
            f'<span class="hc" style="background:color-mix(in srgb, var(--good) 100%, var(--line))"></span> More</div></div>')


def render_analytics(plan, progress):
    acts = gather_activities(progress)
    st.markdown(STYLE + '<div class="sv">' +
                section("Headline stats", "Everything logged so far this build.", analytics_headline_html(acts))
                + "</div>", unsafe_allow_html=True)

    st.markdown(STYLE + '<div class="sv"><div class="sec"><div class="sec-head"><h2>Pace trend</h2>'
                '<p class="sub">Logged pace by session type over time.</p></div></div></div>', unsafe_allow_html=True)
    pdf = pace_trend_df(acts)
    if pdf is not None and not pdf.empty:
        st.line_chart(pdf, height=260)
    else:
        st.caption("Not enough paced runs logged yet.")

    st.markdown(STYLE + '<div class="sv"><div class="sec"><div class="sec-head"><h2>Heart rate trend</h2>'
                '<p class="sub">Average HR per run — falling HR at the same pace is a fitness signal.</p></div></div></div>',
                unsafe_allow_html=True)
    hdf = hr_trend_df(acts)
    if hdf is not None:
        st.line_chart(hdf, height=220, color=["#ce2e3b"])
    else:
        st.caption("Not enough heart-rate data logged yet (needs a HR strap/watch on Strava).")

    ratio_series, current_ratio = acwr_series(plan, progress)
    st.markdown(STYLE + '<div class="sv">' +
                section("Training load (ACWR)", "Acute (7-day) vs chronic (28-day) load ratio.",
                        acwr_band_html(current_ratio) if current_ratio is not None else
                        '<p class="sub">Not enough logged history yet — needs a few weeks of runs.</p>')
                + "</div>", unsafe_allow_html=True)
    if ratio_series is not None:
        st.line_chart(ratio_series.rename("ACWR"), height=200)

    st.markdown(STYLE + '<div class="sv">' +
                section("Race-time prediction", "Riegel formula from your best logged checkpoint/race effort.",
                        predict_html(predict_race_time(progress), plan["meta"].get("goal_note", "")))
                + "</div>", unsafe_allow_html=True)

    st.markdown(STYLE + '<div class="sv">' +
                section("Consistency heatmap", "Every day of the plan so far — darker = more distance.",
                        calendar_heatmap_html(plan, progress)) + "</div>", unsafe_allow_html=True)

    st.markdown(STYLE + '<div class="sv"><div class="sec"><div class="sec-head"><h2>Route map</h2>'
                '<p class="sub">Every logged run with GPS data, plotted together.</p></div></div></div>',
                unsafe_allow_html=True)
    paths = []
    for a in acts:
        pts = decode_polyline(a.get("polyline"))
        if len(pts) > 1:
            paths.append({"path": [[lng, lat] for lat, lng in pts], "name": a.get("name", "")})
    if paths:
        import pydeck as pdk
        all_lats = [p[1] for path in paths for p in path["path"]]
        all_lngs = [p[0] for path in paths for p in path["path"]]
        view = pdk.ViewState(latitude=sum(all_lats) / len(all_lats), longitude=sum(all_lngs) / len(all_lngs), zoom=10)
        layer = pdk.Layer("PathLayer", data=paths, get_path="path", get_color=[206, 46, 59, 160],
                           width_min_pixels=2, pickable=True)
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, map_style=None,
                                  tooltip={"text": "{name}"}))
    else:
        st.caption("No GPS routes logged yet — these appear automatically once Strava activities include location data.")


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
            if res is None:
                st.warning("No Strava creds for this runner (see README).")
            else:
                st.success("Synced!")
                st.rerun()
        except Exception as e:
            st.error(f"Sync failed: {e}")

    # ---- hero (facts strip + glam progress rings) stays fixed above the subtabs ----
    banner = f'<div class="banner">{esc(content["banner"])}</div>' if content.get("banner") else ""
    st.markdown(STYLE + '<div class="sv">' + celebration_html(plan, progress) + banner + facts_html(plan, wk_rows) +
                glam_row_html(plan, progress, cur) + "</div>", unsafe_allow_html=True)

    # ---- everything else lives in subtabs (Diet Plan only shows up if a runner has one) ----
    has_diet = bool(content.get("diet"))
    labels = ["📋 Plan", "🧭 Approach", "🎯 Paces", "🚦 Gates", "📈 Volume", "📊 Analytics",
              "💪 Strength", "🥗 Fuel & life"] + (["🍽️ Diet Plan"] if has_diet else []) + ["💡 Tips", "🔬 Research"]
    sub = st.tabs(labels)
    i = iter(range(len(labels)))

    with sub[next(i)]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("The 33-week plan", "Grouped by phase — open any week for the day-by-day.",
                            LEGEND + weeks_html(plan, progress, cur)) + "</div>", unsafe_allow_html=True)
    with sub[next(i)]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("The approach", "Why the plan is shaped the way it is.", approach_html(plan))
                    + "</div>", unsafe_allow_html=True)
    with sub[next(i)]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("Pace zones", f'Anchored on {plan["meta"]["goal"]} (MP {plan["meta"]["mp_per_km"]}/km).',
                            paces_html(plan)) + "</div>", unsafe_allow_html=True)
    with sub[next(i)]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("Decision gates", "Checkpoints that confirm the plan is on track.", gates_html(plan))
                    + "</div>", unsafe_allow_html=True)
    with sub[next(i)]:
        st.markdown(STYLE + '<div class="sv"><div class="sec"><div class="sec-head"><h2>Weekly volume</h2>'
                    '<p class="sub">Planned vs actual (Strava).</p></div></div></div>', unsafe_allow_html=True)
        if wk_rows:
            rows = [{"Week": wk["week"], "Planned": wk["target_km"],
                     "Actual": wk_rows.get(str(wk["week"]), {}).get("actual_km", 0)} for wk in plan["weeks"]]
            st.bar_chart(pd.DataFrame(rows).set_index("Week"), color=["#c7d2e0", "#2f8f7e"], height=200)
        else:
            st.caption("No synced weeks yet.")
    with sub[next(i)]:
        render_analytics(plan, progress)
    with sub[next(i)]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("Strength &amp; conditioning", "", strength_html(plan)) + "</div>", unsafe_allow_html=True)
    with sub[next(i)]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("Fuel &amp; life", "", fuel_html(plan)) + "</div>", unsafe_allow_html=True)
    if has_diet:
        with sub[next(i)]:
            st.markdown(STYLE + '<div class="sv">' +
                        section("Diet plan — building a surplus", "Meals, add-ins and targets to gain weight safely as volume climbs.",
                                diet_html(plan)) + "</div>", unsafe_allow_html=True)
    with sub[next(i)]:
        st.markdown(STYLE + '<div class="sv">' +
                    section("Tips", "", tips_html(plan)) + "</div>", unsafe_allow_html=True)
    with sub[next(i)]:
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
