#!/usr/bin/env python3
"""
Self-Improvement Review Agent
Reviews company performance and identifies improvements
Now includes Lead Gen + Pipeline analysis
"""
import os
import json
from datetime import datetime
from collections import Counter

CRM_FILE = "/tmp/company_crm.json"
LEARN_STATE = "/tmp/learn_state.json"
LOG_FILE = "/tmp/self_review.log"
IMPROVEMENTS_FILE = "/tmp/improvements.json"
LEADS_FILE = "/tmp/leads.json"
PIPELINE_FILE = "/tmp/sales_pipeline.json"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

def analyze_performance():
    """Analyze company performance"""
    
    # Load data
    crm = load_json(CRM_FILE, {"leads": [], "activities": [], "pipeline": [], "tasks": []})
    learn = load_json(LEARN_STATE, {"topics_done": [], "actions_done": []})
    leads = load_json(LEADS_FILE, {"leads": []})
    pipeline = load_json(PIPELINE_FILE, {"deals": []})
    
    topics = learn.get("topics_done", [])
    actions = learn.get("actions_done", [])
    activities = crm.get("activities", [])
    
    # Analysis
    issues = []
    improvements = []
    
    # Learning stats
    if len(topics) > 0:
        improvements.append(f"📚 Learning: {topics[-1]} ({len(topics)} topics)")
    
    if len(actions) > 0:
        improvements.append(f"⚡ Actions: {actions[-1]} ({len(actions)} total)")
    
    # Lead Gen analysis
    total_leads = len(leads.get("leads", []))
    leads_clicked = sum(1 for l in leads.get("leads", []) if l.get("clicked"))
    leads_replied = sum(1 for l in leads.get("leads", []) if l.get("replied"))
    
    if total_leads > 0:
        improvements.append(f"🎯 Leads: {total_leads} generated ({leads_clicked} clicked, {leads_replied} replied)")
    else:
        issues.append("❌ No leads generated")
    
    # Pipeline analysis
    deals = pipeline.get("deals", [])
    pipeline_value = sum(d.get("value", 0) for d in deals)
    pipeline_by_stage = Counter([d["stage"] for d in deals])
    
    if len(deals) > 0:
        improvements.append(f"💼 Pipeline: {len(deals)} deals, ${pipeline_value} value")
        improvements.append(f"   Stages: {dict(pipeline_by_stage)}")
    else:
        issues.append("❌ No pipeline deals")
    
    # Check for conversions
    closed_won = pipeline_by_stage.get("closed_won", 0)
    if closed_won > 0:
        improvements.append(f"🎉 CLOSED {closed_won} DEALS!")
    else:
        issues.append("⚠️ No deals closed yet")
    
    # High activity but low results
    if len(actions) > 100 and total_leads == 0:
        issues.append("⚠️ High actions but no lead conversion")
    
    # Summary
    result = {
        "timestamp": datetime.now().isoformat(),
        "stats": {
            "topics": len(topics),
            "actions": len(actions),
            "leads": total_leads,
            "leads_clicked": leads_clicked,
            "leads_replied": leads_replied,
            "pipeline_deals": len(deals),
            "pipeline_value": pipeline_value,
            "closed_won": closed_won
        },
        "issues": issues,
        "improvements": improvements
    }
    
    return result

def main():
    log("🔍 Starting self-improvement review...")
    
    result = analyze_performance()
    
    log(f"📊 Stats: {result['stats']}")
    
    # Print report
    print("\n" + "="*50)
    print("🔍 EVERYCOMPANYCLAW - WEEKLY REVIEW")
    print("="*50)
    print(f"\n📊 PERFORMANCE:")
    print(f"   Topics: {result['stats']['topics']}")
    print(f"   Actions: {result['stats']['actions']}")
    print(f"   Leads Generated: {result['stats']['leads']}")
    print(f"   Leads Clicked: {result['stats']['leads_clicked']}")
    print(f"   Leads Replied: {result['stats']['leads_replied']}")
    print(f"   Pipeline Deals: {result['stats']['pipeline_deals']}")
    print(f"   Pipeline Value: ${result['stats']['pipeline_value']}")
    print(f"   Closed Won: {result['stats']['closed_won']}")
    
    print(f"\n❌ ISSUES:")
    for issue in result['issues']:
        print(f"   {issue}")
    
    print(f"\n✅ IMPROVEMENTS:")
    for imp in result['improvements']:
        print(f"   {imp}")
    
    print("\n" + "="*50)
    
    # Save
    with open(IMPROVEMENTS_FILE, "w") as f:
        json.dump(result, f, indent=2)
    
    print("\n✅ Review complete!")

if __name__ == "__main__":
    main()
