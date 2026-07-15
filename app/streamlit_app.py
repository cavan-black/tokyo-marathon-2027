#!/usr/bin/env python3
"""Shared Tokyo Marathon dashboard — one tab per runner, planned vs actual, Strava-synced."""
import os, sys, json, html
from datetime import date, datetime

import pandas as pd
import streamlit as st

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, ROOT)

st.set_page_config(page_title="Tokyo 2027 · Team dashboard", page_icon="🏃", layout="wide")

COLOR = {"Done": "#16a34a", "Partial": "#d97706", "Missed": "#dc2626",
         "Rest": "#9ca3af", "Upcoming": "#cbd5e1", "—": "#cbd5e1"}

st.markdown("""<style>
.pj-day{display:flex;align-items:center;gap:.65rem;padding:.5rem .8rem;margin:.28rem 0;
  border-radius:12px;border-left:5px solid #cbd5e1;background:rgba(130,130,150,.07);}
.pj-dot{width:9px;height:9px;border-radius:50%;flex:0 0 auto}
.pj-date{font-weight:700;font-size:.72rem;min-width:82px;letter-spacing:.03em;opacity:.7;text-transform:uppercase}
.pj-sess{flex:1 1 auto;font-size:.9rem;line-height:1.3}
.pj-pills{display:flex;gap:.35rem;flex:0 0 auto;flex-wrap:wrap;justify-content:flex-end}
.pj-pill{font-size:.68rem;padding:.13rem .5rem;border-radius:999px;background:rgba(130,130,150,.16);
  white-space:nowrap;font-weight:600}
.pj-pill.act{background:rgba(22,163,74,.18);color:#16a34a}
.pj-rest{opacity:.5}
.pj-banner{padding:.7rem 1rem;border-radius:12px;background:rgba(217,160,0,.14);
  border-left:5px solid #d9a200;font-size:.85rem;margin:.3rem 0 .9rem}
</style>""", unsafe_allow_html=True)


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


def show_table(headers, rows):
    st.dataframe(pd.DataFrame(rows, columns=headers), hide_index=True, use_container_width=True)


def day_card(d, pd_, today_iso):
    status = pd_.get("status") or ("Rest" if d["type"] == "rest"
                                   else ("Upcoming" if d["date"] > today_iso else "—"))
    color = COLOR.get(status, "#cbd5e1")
    dt = datetime.fromisoformat(d["date"]).strftime("%a %d %b")
    pills = f'<span class="pj-pill">🎯 {d["target_km"]:g} km</span>' if d["target_km"] else ""
    actual, pace = pd_.get("actual_km", 0), pd_.get("pace_str")
    if actual:
        pills += f'<span class="pj-pill act">✓ {actual:.1f} km{(" · " + pace + "/km") if pace else ""}</span>'
    rest = " pj-rest" if status == "Rest" else ""
    return (f'<div class="pj-day{rest}" style="border-left-color:{color}">'
            f'<span class="pj-dot" style="background:{color}"></span>'
            f'<span class="pj-date">{dt}</span>'
            f'<span class="pj-sess">{html.escape(d["session"])}</span>'
            f'<span class="pj-pills">{pills}</span></div>')


def plan_tab(plan, progress):
    content = plan.get("content", {})
    if content.get("banner"):
        st.markdown(f'<div class="pj-banner">{html.escape(content["banner"])}</div>', unsafe_allow_html=True)
    meta = plan["meta"]; today = date.today(); today_iso = today.isoformat()
    wk_rows = progress.get("weeks", {})
    tr = progress.get("tracker")
    if tr and (tr.get("threshold_latest") or tr.get("mp_latest")):
        t1, t2 = st.columns(2)
        lt, lm = tr.get("threshold_latest"), tr.get("mp_latest")
        t1.metric("Latest threshold pace", (lt[1] + "/km") if lt else "—", "comfortably-hard efforts", delta_color="off")
        t2.metric("Latest MP / long pace", (lm[1] + "/km") if lm else "—", f'MP target {meta["mp_per_km"]}/km', delta_color="off")
    if wk_rows:
        rows = [{"Week": wk["week"], "Planned": wk["target_km"],
                 "Actual": wk_rows.get(str(wk["week"]), {}).get("actual_km", 0)} for wk in plan["weeks"]]
        st.markdown("**Weekly volume — planned vs actual**")
        st.bar_chart(pd.DataFrame(rows).set_index("Week"), color=["#c7d2e0", "#16a34a"], height=200)
    cur = next((wk["week"] for wk in plan["weeks"]
                if datetime.fromisoformat(wk["start"]).date() <= today
                <= datetime.fromisoformat(wk["start"]).date() + pd.Timedelta(days=6)), 1)
    st.caption("🟢 done · 🟠 partial · 🔴 missed · ⚪ rest · ▫️ upcoming · 🎯 target · ✓ actual")
    for wk in plan["weeks"]:
        wsum = wk_rows.get(str(wk["week"]), {})
        label = (f"Week {wk['week']} · {wk['start']} · {wk['phase']} · {wk['target_km']} km"
                 + (f"  —  {wk['focus']}" if wk['focus'] else ""))
        with st.expander(label, expanded=(wk["week"] == cur)):
            if wsum:
                m = st.columns(4)
                m[0].metric("Planned km", f'{wsum["planned_km"]:.0f}')
                m[1].metric("Actual km", f'{wsum["actual_km"]:.0f}')
                m[2].metric("Quality hit", f'{wsum["quality_hit"]}/{wsum["quality_planned"]}')
                m[3].metric("Sessions ✓", wsum["done"])
                flag = wsum.get("flag", "")
                color = "#16a34a" if flag.startswith("✓") else "#d9a200"
                st.markdown(f"<span style='color:{color};font-weight:600'>{html.escape(flag)}</span>", unsafe_allow_html=True)
            html_days = "".join(day_card(d, progress.get("days", {}).get(d["date"], {}), today_iso) for d in wk["days"])
            st.markdown(html_days, unsafe_allow_html=True)


def render_runner(runner_id):
    plan = load_json(f"plan_{runner_id}.json")
    if not plan:
        st.error(f"No plan for {runner_id} — run plan/plan_generator.py."); return
    progress = load_json(f"progress_{runner_id}.json",
                         {"days": {}, "weeks": {}, "last_sync": None, "tracker": None})
    meta = plan["meta"]; content = plan.get("content", {})
    today = date.today(); race_day = datetime.fromisoformat(meta["race"]).date()
    wk_rows = progress.get("weeks", {})

    c = st.columns(4)
    c[0].metric("Goal", meta["goal"], f'{meta["mp_per_km"]}/km')
    c[1].metric("Race day", race_day.strftime("%d %b %Y"), f"{(race_day - today).days} days to go")
    done_total = sum(w["done"] for w in wk_rows.values())
    due = sum(w["done"] + w["partial"] + w["missed"] for w in wk_rows.values())
    c[2].metric("Sessions ✓", done_total, f"of {due} due so far" if due else "—")
    c[3].metric("Km logged", f'{sum(w["actual_km"] for w in wk_rows.values()):.0f}', "since start")
    st.caption(meta.get("goal_note", ""))

    a, b = st.columns([3, 1])
    a.caption(f"Last Strava sync: {progress.get('last_sync') or 'never — connect Strava or hit refresh'}")
    if b.button("🔄 Refresh from Strava", key=f"r_{runner_id}", use_container_width=True):
        try:
            with st.spinner("Pulling from Strava…"):
                res = refresh_runner(runner_id)
            st.warning("No Strava creds for this runner (see README).") if res is None else (st.success("Synced!"), st.rerun())
        except Exception as e:
            st.error(f"Sync failed: {e}")

    tabs = st.tabs(["📋 Plan", "🎯 Paces", "📊 Checkpoints", "💪 Strength", "🥗 Fuel & Life", "💡 Tips"])
    with tabs[0]:
        plan_tab(plan, progress)
    with tabs[1]:
        p = content.get("paces", {})
        if p:
            show_table(p["headers"], p["rows"])
            if p.get("note"): st.caption(p["note"])
        if content.get("goals"):
            st.markdown("**Your goals — pick MP off the checkpoints**")
            g = content["goals"]; show_table(g["headers"], g["rows"])
    with tabs[2]:
        cp = content.get("checkpoints", {})
        if cp:
            if cp.get("intro"): st.info(cp["intro"])
            show_table(cp["headers"], cp["rows"])
            for n in cp.get("notes", []):
                st.markdown(f"- {n}")
    with tabs[3]:
        sc = content.get("strength", {})
        if sc:
            st.caption(sc.get("intro", ""))
            for blk in sc.get("blocks", []):
                st.markdown(f"**{blk['title']}**")
                if blk.get("note"): st.caption(blk["note"])
                show_table(blk["headers"], blk["rows"])
    with tabs[4]:
        fu = content.get("fuel", {})
        if fu:
            st.caption(fu.get("intro", ""))
            for sec in fu.get("sections", []):
                st.markdown(f"**{sec['title']}**")
                show_table(sec["headers"], sec["rows"])
    with tabs[5]:
        show_table(["Topic", "Detail"], content.get("tips", []))


# ---------------- page ----------------
st.title("🏃 Tokyo Marathon 2027 — Team dashboard")
runners = load_json("runners.json", [])
if not runners:
    st.error("No runners.json — run: python plan/plan_generator.py")
else:
    for tab, r in zip(st.tabs([f'{r["name"]} · {r["goal"]}' for r in runners]), runners):
        with tab:
            render_runner(r["id"])
st.divider()
st.caption("Adjustments are suggestions — you decide. Data © each runner, via Strava (personal use). "
           "Auto-syncs a few times a day; hit refresh for on-demand.")
