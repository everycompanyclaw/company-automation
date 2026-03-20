#!/usr/bin/env python3
"""
Live CRM Dashboard - Real-time company visualization
"""
import os
import json
from datetime import datetime

CRM_FILE = "/tmp/company_crm.json"
LOG_FILE = "/tmp/aggressive_learn.log"

def load_crm():
    """Load CRM data"""
    if os.path.exists(CRM_FILE):
        with open(CRM_FILE, "r") as f:
            return json.load(f)
    return {
        "leads": [],
        "activities": [],
        "pipeline": [],
        "tasks": []
    }

def save_crm(data):
    """Save CRM data"""
    with open(CRM_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_lead(name, source, status="new"):
    """Add a new lead"""
    crm = load_crm()
    lead = {
        "id": len(crm["leads"]) + 1,
        "name": name,
        "source": source,
        "status": status,
        "added": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "last_contact": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    crm["leads"].append(lead)
    save_crm(crm)
    return lead

def add_activity(action, details):
    """Add activity log"""
    crm = load_crm()
    activity = {
        "id": len(crm["activities"]) + 1,
        "action": action,
        "details": details,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    crm["activities"].append(activity)
    # Keep last 50 activities
    crm["activities"] = crm["activities"][-50:]
    save_crm(crm)
    return activity

def update_pipeline(stage, item):
    """Update sales pipeline"""
    crm = load_crm()
    pipeline_item = {
        "stage": stage,
        "item": item,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    # Remove if exists
    crm["pipeline"] = [p for p in crm["pipeline"] if p["item"] != item]
    crm["pipeline"].append(pipeline_item)
    save_crm(crm)
    return pipeline_item

def get_dashboard():
    """Get dashboard data"""
    crm = load_crm()
    
    # Get last 10 activities
    recent = crm["activities"][-10:]
    
    # Count leads by status
    lead_counts = {}
    for lead in crm["leads"]:
        status = lead["status"]
        lead_counts[status] = lead_counts.get(status, 0) + 1
    
    return {
        "total_leads": len(crm["leads"]),
        "lead_counts": lead_counts,
        "recent_activities": recent,
        "pipeline": crm["pipeline"]
    }

def generate_marketing_content():
    """Generate content for the company"""
    crm = load_crm()
    
    posts = [
        "🧠 We help businesses automate their workflows and save 10+ hours/week. DM us!",
        "🤖 Automation is the future. What's your manual task? Let's automate it!",
        "💡 Stop doing the same thing twice. Automate it once!",
        "⚡ Python scripts, Zapier templates, AI prompts - we got you!",
        "📈 Save time, make money. Automation for small business.",
    ]
    
    for post in posts:
        add_activity("content_created", post)
    
    return posts

if __name__ == "__main__":
    # Test
    add_activity("system_start", "CRM initialized")
    add_lead("Startup Founder", "LinkedIn")
    dashboard = get_dashboard()
    print(json.dumps(dashboard, indent=2))
