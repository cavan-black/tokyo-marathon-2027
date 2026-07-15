#!/usr/bin/env python3
"""Build every runner's plan JSON + a runners manifest. Run: python plan/plan_generator.py"""
import os, sys, json

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, HERE)

import cav, jamie  # noqa: E402

RUNNERS = [cav, jamie]

if __name__ == "__main__":
    os.makedirs(DATA, exist_ok=True)
    manifest = []
    for mod in RUNNERS:
        plan = mod.build()
        m = plan["meta"]
        with open(os.path.join(DATA, f"plan_{m['id']}.json"), "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        manifest.append({"id": m["id"], "name": m["name"], "goal": m["goal"]})
        nd = sum(1 for wk in plan["weeks"] for d in wk["days"] if d["type"] != "rest")
        print(f"  {m['name']}: 33 weeks, {nd} training days, peak {m['peak_km']} km")
    with open(os.path.join(DATA, "runners.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(manifest)} runner plans + runners.json")
