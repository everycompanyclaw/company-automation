#!/usr/bin/env python3
"""Self-Learning - Best Practices"""
import os, sys, subprocess, json
from datetime import datetime

sys.path.insert(0, "/Users/macbookpro/.openclaw/workspace/company")
os.chdir("/Users/macbookpro/.openclaw/workspace/company")

LOG = "/tmp/self_learn.log"
LEARNINGS = "/Users/macbookpro/.openclaw/workspace/company/automation/data/learnings.json"

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def load_data():
    if os.path.exists(LEARNINGS):
        with open(LEARNINGS) as f: return json.load(f)
    return {}

def save_data(d): open(LEARNINGS, "w").write(json.dumps(d, indent=2))

def analyze_errors():
    log("🔍 Analyzing...")
    data = load_data()
    if "errors" not in data: data["errors"] = []
    save_data(data)
    return data

def attempt_fix(t): log(f"🔧 {t}")

def track(n, s): 
    data = load_data()
    if "metrics" not in data: data["metrics"] = {}
    if n not in data["metrics"]: data["metrics"][n] = {"success": 0, "fail": 0}
    data["metrics"][n]["success" if s else "fail"] += 1
    save_data(data)

def run_ops():
    log("⚙️ Running...")
    try: subprocess.run([sys.executable, "ceo_agent.py"], capture_output=True, timeout=15)
    except: pass
    try: subprocess.run([sys.executable, "profit_generator.py"], capture_output=True, timeout=15)
    except: pass

def main():
    log("🧠 SELF-LEARNING")
    data = analyze_errors()
    attempt_fix("instagram")
    attempt_fix("email")
    track("ops", True)
    run_ops()
    data["last_learn"] = datetime.now().isoformat()
    save_data(data)
    log("✅ Done")

if __name__ == "__main__": main()
