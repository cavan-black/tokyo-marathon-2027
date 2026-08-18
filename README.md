# Tokyo Marathon 2027 — Team Dashboard

Interactive, Strava-synced training dashboard for **Cav** (sub-2:50) and **Jamie**
(4:00 → reach 3:30). One shared page, a tab per runner: planned vs actual, weekly
volume chart, quality-session tracking, pace signal, and a coach-style flag per week.

- Auto-syncs from Strava **a few times a day** (GitHub Actions cron)
- **On-demand** refresh button in the dashboard
- Free to host (Streamlit Community Cloud + GitHub Actions)

The plan is generated from data (`plan/cav.py`, `plan/jamie.py`) — the same source
of truth behind the Excel plans. Edit a plan there and re-run the generator.

```
marathon-dash/
  plan/       cav.py, jamie.py, plan_generator.py   # plans as data -> data/plan_<id>.json
  sync/       strava.py, match.py, manual.py, run_sync.py, get_token.py
  app/        streamlit_app.py                       # the dashboard (tabs per runner)
  data/       plan_*.json, progress_*.json, runners.json
  .github/workflows/sync.yml                         # scheduled + on-demand sync
```

---

## 1. Run it locally (5 min)

```bash
pip install -r requirements.txt
python plan/plan_generator.py          # writes data/plan_*.json + runners.json
streamlit run app/streamlit_app.py     # opens http://localhost:8501
```

Without Strava creds it shows the full plan with every session "upcoming" — that's
the correct pre-start state. Connect Strava to light it up.

## 2. Connect Strava (one API app, once per runner)

1. Create an API application at <https://www.strava.com/settings/api>
   - **Authorization Callback Domain:** `localhost`
   - Note the **Client ID** and **Client Secret**.
2. `cp .env.example .env` and fill in `STRAVA_CLIENT_ID` / `STRAVA_CLIENT_SECRET`.
3. Get each runner's refresh token (that person logs in when the browser opens):
   ```bash
   python sync/get_token.py cav      # Cav authorises  -> STRAVA_REFRESH_TOKEN_CAV
   python sync/get_token.py jamie    # Jamie authorises -> STRAVA_REFRESH_TOKEN_JAMIE
   ```
   Paste each printed token into `.env`.
4. Test a sync: `python sync/run_sync.py` → writes `data/progress_*.json`.
   Reload the dashboard.

> Personal, single-user use is within Strava's API terms. Note their Nov-2024 rules:
> don't display other people's data to third parties, and **don't feed Strava data
> into AI/ML models**. This app does neither — matching is plain rules.

## 3. Host it free (Streamlit Community Cloud)

1. Put this folder in a **GitHub repo** (private is fine):
   ```bash
   git init && git add . && git commit -m "marathon dashboard"
   git branch -M main && git remote add origin <your-repo-url> && git push -u origin main
   ```
2. Go to <https://share.streamlit.io> → **New app** → pick the repo →
   main file `app/streamlit_app.py` → Deploy.
3. In the app's **Settings → Secrets**, paste (TOML):
   ```toml
   STRAVA_CLIENT_ID = "12345"
   STRAVA_CLIENT_SECRET = "…"
   STRAVA_REFRESH_TOKEN_CAV = "…"
   STRAVA_REFRESH_TOKEN_JAMIE = "…"
   STRAVA_REFRESH_TOKEN_STEPHEN = "…"
   STRAVA_REFRESH_TOKEN_AMBER = "…"
   GH_PAT = "…"
   ```
   (Only set the tokens for runners who've actually connected Strava — a missing one
   just means that runner's tab shows everything as "upcoming" until they do.)
   The **🔄 Refresh from Strava** button now works live.

   `GH_PAT` is optional but recommended: Streamlit Cloud's filesystem is ephemeral, so a
   manual refresh that only writes locally gets **wiped the next time the app redeploys**
   (which happens on every push to the repo, including the scheduled sync a few hours
   later) — it'll look like it worked, then quietly revert. With `GH_PAT` set, a manual
   refresh commits `data/progress_<id>.json` straight to GitHub via their API, so it
   persists the same way the scheduled sync's commits do. Create one at
   <https://github.com/settings/tokens> (fine-grained token scoped to just this repo,
   **Contents: Read and write** permission is enough) and paste it in as `GH_PAT`.
   Without it, the button still works for the current session — you just won't see it
   survive a redeploy.

## 4. Auto-sync a few times a day (GitHub Actions)

`.github/workflows/sync.yml` runs at 06:00 / 13:00 / 21:00 UTC and on demand. In your
GitHub repo → **Settings → Secrets and variables → Actions**, add `STRAVA_CLIENT_ID`,
`STRAVA_CLIENT_SECRET` and one `STRAVA_REFRESH_TOKEN_<RUNNER>` per connected runner —
the same values as the `.env` above, minus `GH_PAT` (Actions commits with its own
token). The workflow pulls Strava, rebuilds `data/progress_*.json`, and commits it;
Streamlit Cloud auto-redeploys on the new commit. Trigger a manual run any time from the
**Actions** tab → *Strava sync* → *Run workflow*.

Three things worth knowing about it:

- It commits on **every** run, because `last_sync` changes each time — that's what keeps
  the dashboard's "last synced" honest, at the cost of three commits a day.
- GitHub **disables scheduled workflows after 60 days with no repo activity**, and queues
  scheduled runs on a best-effort basis, so they drift by a few minutes. Neither matters
  much for a training log, but a silently-paused sync looks identical to a quiet week.
- If Strava ever rotates a refresh token, the run can only *print* the new one — nothing
  in Actions can rewrite a repo secret. The workflow raises a warning on the run summary
  when that happens; update the secret or every later run fails to authenticate.

## Sessions with no device behind them

A BJJ class, a pickup game, a swim on a dead watch — nothing reaches Strava, so the day
reads "Missed" and drags the week's coach flag with it. Write those down in
`data/manual_<runner>.json` and the sync folds them in:

```json
[
  {"date": "2026-08-18", "activity_type": "MartialArts",
   "name": "BJJ sparring", "moving_time_s": 10800, "note": "3 h, no device"}
]
```

`date`, `activity_type` and `moving_time_s` are required; `activity_type` must be one of
`sync/strava.py`'s `CROSS_TYPES`. The file is read on every sync, so an entry keeps
applying — and it's dropped automatically if the same activity type later turns up from
Strava on that date, so a late-syncing watch doesn't double-count the day.

Two deliberate limits. **Manual entries are cross-training only** — they can satisfy a day
(a "Substituted" status, whose km come off the week's runnable denominator) but never add
running km or ACWR load, because a training-load signal you can type into isn't a signal.
And **writing an entry by hand grants it no privilege a recorded one wouldn't have**: the
same cardio rule applies, so a hand-entered gym session still doesn't cover a run. Every
such session is marked "✎ by hand" in the dashboard rather than passing as measured.

## Editing the plan

Adjust `plan/cav.py` or `plan/jamie.py` (volumes `VOL`, long runs `LR`, or session text),
then `python plan/plan_generator.py`. The weekly **flag** in the dashboard ("under-target /
hold", "on track") is a *suggestion* — you decide what to change. Keep a human in the loop;
don't let one bad week auto-rewrite the block.
