#!/usr/bin/env python3
"""
Update status.json with real company data and push to GitHub
"""
import json
import os
import subprocess

LEARN_STATE = "/tmp/learn_state.json"
CRM_FILE = "/tmp/company_crm.json"
STATUS_FILE = "/Users/macbookpro/.openclaw/workspace/company/status.json"
GIT_DIR = "/Users/macbookpro/.openclaw/workspace/company"

def update_status():
    """Update status.json with real data and push to GitHub"""
    
    # Load learning state
    learn_state = {"topics_done": [], "actions_done": []}
    if os.path.exists(LEARN_STATE):
        with open(LEARN_STATE, "r") as f:
            learn_state = json.load(f)
    
    topics = learn_state.get("topics_done", [])
    actions = learn_state.get("actions_done", [])
    
    # Load CRM
    crm = {"leads": [], "activities": [], "pipeline": []}
    if os.path.exists(CRM_FILE):
        with open(CRM_FILE, "r") as f:
            crm = json.load(f)
    
    # Build activities
    activities = []
    for act in crm.get("activities", [])[-5:]:
        activities.append({
            "time": act.get("time", "")[:5],
            "action": act.get("action", ""),
            "details": act.get("details", "")[:40]
        })
    
    # Add recent learning actions
    if len(activities) < 5:
        for act in actions[-5:]:
            activities.append({
                "time": "now",
                "action": "doing",
                "details": f"Executed: {act}"
            })
    
    # Build status
    status = {
        "current_topic": topics[-1] if topics else "marketing",
        "current_action": actions[-1] if actions else "growing",
        "topics_count": len(topics),
        "actions_count": len(actions),
        "leads_count": len(crm.get("leads", [])),
        "pipeline_count": len(crm.get("pipeline", [])),
        "activities": activities
    }
    
    # Save
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)
    
    # Commit and push
    try:
        subprocess.run(["git", "-C", GIT_DIR, "add", "status.json"], check=True)
        subprocess.run(["git", "-C", GIT_DIR, "commit", "-m", "Update live status"], check=True)
        subprocess.run(["git", "-C", GIT_DIR, "push", "origin", "main:gh-pages"], check=True)
        print(f"✅ Updated and pushed: {status['topics_count']} topics, {status['actions_count']} actions")
    except Exception as e:
        print(f"⚠️ Updated locally but push failed: {e}")

if __name__ == "__main__":
    update_status()
