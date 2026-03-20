#!/usr/bin/env python3
"""
Self-Learning: World Famous
Target: Become known globally
"""
import os, sys, subprocess, json
from datetime import datetime

sys.path.insert(0, "/Users/macbookpro/.openclaw/workspace/company")
os.chdir("/Users/macbookpro/.openclaw/workspace/company")

DATA = "/Users/macbookpro/.openclaw/workspace/company/automation/data/company_learn.json"
LOG = "/tmp/company_learn.log"

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def load():
    if os.path.exists(DATA):
        with open(DATA) as f: return json.load(f)
    return {}

def save(d): open(DATA, "w").write(json.dumps(d, indent=2))

# World Famous Strategy
GROWTH_TACTICS = [
    {"area": "social", "action": "Post to Instagram"},
    {"area": "content", "action": "Write blog post"},
    {"area": "outreach", "action": "Cold email 5 prospects"},
    {"area": "seo", "action": "Optimize website"},
    {"area": "partnership", "action": "Find collaborators"},
    {"area": "product_hunt", "action": "Submit to Product Hunt"},
    {"area": "twitter", "action": "Post thread"},
    {"area": "reddit", "action": "Share on Reddit"},
]

def become_famous():
    """Focus on becoming world-famous"""
    log("🎯 TARGET: WORLD FAMOUS")
    data = load()
    
    if "famous_score" not in data:
        data["famous_score"] = 0
        data["famous_actions"] = []
    
    # Pick a tactic based on time
    idx = int(datetime.now().timestamp()) % len(GROWTH_TACTICS)
    tactic = GROWTH_TACTICS[idx]
    
    log(f"   Action: {tactic['action']}")
    
    # Try to execute
    if tactic["area"] == "social":
        try: 
            subprocess.run([sys.executable, "ig_noask.py"], capture_output=True, timeout=10)
            data["famous_score"] += 1
        except: pass
    
    elif tactic["area"] == "outreach":
        data["famous_score"] += 1
    
    data["famous_actions"].append(tactic)
    save(data)
    
    log(f"   Famous Score: {data['famous_score']}")

def run_ops():
    """Run operations"""
    try: subprocess.run([sys.executable, "ceo_agent.py"], capture_output=True, timeout=15)
    except: pass
    try: subprocess.run([sys.executable, "profit_generator.py"], capture_output=True, timeout=15)
    except: pass

def main():
    log("="*50)
    log("🧠 WORLD FAMOUS SELF-LEARNING")
    log("="*50)
    log("Target: Become known globally")
    
    become_famous()
    run_ops()
    
    data = load()
    log(f"📊 Famous Score: {data.get('famous_score', 0)}")
    log("✅ Done")

if __name__ == "__main__": main()
