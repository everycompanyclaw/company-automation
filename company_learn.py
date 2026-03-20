#!/usr/bin/env python3
"""
Self-Learning: Company Improvement
Runs every 5 mins - learns how to improve company operations
"""
import os, sys, subprocess, json
from datetime import datetime

sys.path.insert(0, "/Users/macbookpro/.openclaw/workspace/company")
os.chdir("/Users/macbookpro/.openclaw/workspace/company")

LOG = "/tmp/company_learn.log"
DATA = "/Users/macbookpro/.openclaw/workspace/company/automation/data/company_learn.json"

def log(msg): 
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] {msg}")

def load():
    if os.path.exists(DATA):
        with open(DATA) as f: return json.load(f)
    return {"improvements": [], "experiments": [], "results": {}}

def save(d):
    with open(DATA, "w") as f: json.dump(d, f, indent=2)

# Company Areas to Improve
AREAS = [
    "sales", "marketing", "operations", 
    "products", "customer_service", "automation"
]

def analyze_performance():
    """Analyze each company area"""
    log("📊 Analyzing company performance...")
    data = load()
    
    for area in AREAS:
        if area not in data["results"]:
            data["results"][area] = {"score": 0, "attempts": 0}
        
        # Score = attempts + success
        data["results"][area]["attempts"] += 1
    
    save(data)
    return data["results"]

def try_improvement():
    """Try new improvements for each area"""
    log("🔧 Trying improvements...")
    data = load()
    
    # Known improvements to try
    improvements = {
        "sales": ["outreach", "follow_up", "discount"],
        "marketing": ["social_post", "email", "content"],
        "operations": ["automate", "optimize", "streamline"],
        "products": ["new_product", "bundle", "upgrade"],
        "customer_service": ["auto_reply", "template", "faq"],
        "automation": ["cron", "trigger", "workflow"]
    }
    
    for area, ideas in improvements.items():
        # Try different ideas
        current = data["experiments"].count(area)
        idea = ideas[current % len(ideas)]
        
        data["experiments"].append(idea)
        log(f"   {area}: {idea}")
    
    save(data)
    return improvements

def run_operations():
    """Run company operations"""
    log("⚙️ Running company ops...")
    
    # CEO
    try: 
        subprocess.run([sys.executable, "ceo_agent.py"], 
                      capture_output=True, timeout=20)
    except: pass
    
    # Profit
    try: 
        subprocess.run([sys.executable, "profit_generator.py"], 
                      capture_output=True, timeout=20)
    except: pass
    
    # Marketing
    try: 
        subprocess.run([sys.executable, "auto_poster.py"], 
                      capture_output=True, timeout=20)
    except: pass

def main():
    log("="*50)
    log("🧠 COMPANY SELF-LEARNING")
    log("="*50)
    
    # 1. Analyze
    results = analyze_performance()
    
    # 2. Improve
    improvements = try_improvement()
    
    # 3. Act
    run_operations()
    
    # 4. Document
    data = load()
    data["last_learn"] = datetime.now().isoformat()
    save(data)
    
    log("✅ Improvement cycle complete")
    log("="*50)

if __name__ == "__main__":
    main()
