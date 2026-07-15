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
  sync/       strava.py, match.py, run_sync.py, get_token.py
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
   ```
   The **🔄 Refresh from Strava** button now works live.

## 4. Auto-sync a few times a day (GitHub Actions)

Already configured in `.github/workflows/sync.yml` (06:00 / 13:00 / 21:00 UTC + manual).
In your GitHub repo → **Settings → Secrets and variables → Actions**, add the same four
secrets as above. The workflow pulls Strava, rebuilds `data/*.json`, and commits it;
Streamlit Cloud auto-redeploys on the new commit. Trigger a manual run any time from the
**Actions** tab → *Strava sync* → *Run workflow*.

## Editing the plan

Adjust `plan/cav.py` or `plan/jamie.py` (volumes `VOL`, long runs `LR`, or session text),
then `python plan/plan_generator.py`. The weekly **flag** in the dashboard ("under-target /
hold", "on track") is a *suggestion* — you decide what to change. Keep a human in the loop;
don't let one bad week auto-rewrite the block.
