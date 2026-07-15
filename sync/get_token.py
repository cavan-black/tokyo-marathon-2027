#!/usr/bin/env python3
"""ONE-TIME helper to obtain your Strava refresh token.

1. Create an API app at https://www.strava.com/settings/api
   (Authorization Callback Domain: localhost)
2. Put STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET in .env (or the env).
3. Run (once per runner, that person logs in): python sync/get_token.py cav
4. Open the printed URL, click Authorize, you'll be redirected to a
   localhost URL that fails to load — copy the `code=...` value from it.
5. Paste the code here. The script prints STRAVA_REFRESH_TOKEN_<RUNNER>.
"""
import os
import sys
import requests

RUNNER = (sys.argv[1] if len(sys.argv) > 1 else "cav").upper()

def load_env():
    if os.path.exists(".env"):
        for line in open(".env", encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env()
cid = os.environ.get("STRAVA_CLIENT_ID") or input("Client ID: ").strip()
csecret = os.environ.get("STRAVA_CLIENT_SECRET") or input("Client Secret: ").strip()

auth_url = (
    "https://www.strava.com/oauth/authorize?"
    f"client_id={cid}&response_type=code&redirect_uri=http://localhost/exchange_token"
    "&approval_prompt=force&scope=read,activity:read_all"
)
print("\n1) Open this URL and click Authorize:\n\n" + auth_url + "\n")
print("2) You'll be redirected to a localhost page that won't load — that's fine.")
code = input("3) Paste the `code` value from the redirected URL here: ").strip()

r = requests.post("https://www.strava.com/oauth/token", data={
    "client_id": cid, "client_secret": csecret,
    "code": code, "grant_type": "authorization_code",
}, timeout=30)
r.raise_for_status()
tok = r.json()
print("\n=== SUCCESS ===")
print(f"STRAVA_REFRESH_TOKEN_{RUNNER}=" + tok["refresh_token"])
print("\nAdd that to your .env and to your Streamlit / GitHub Actions secrets.")
