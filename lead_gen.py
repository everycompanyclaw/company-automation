#!/usr/bin/env python3
"""
Lead Gen + Sales Pipeline Agent
Scrapes leads, sends outreach, tracks pipeline
"""
import os
import json
import random
import time
from datetime import datetime, timedelta
import requests

PIPELINE_FILE = "/tmp/sales_pipeline.json"
LEADS_FILE = "/tmp/leads.json"
LOG_FILE = "/tmp/lead_gen.log"

# Sample lead sources (in production, scrape real sources)
SAMPLE_LEADS = [
    {"name": "Tech Startup Founder", "company": "StartupXYZ", "email": "founder@startupxyz.com", "source": "linkedin"},
    {"name": "Marketing Manager", "company": "GrowthCo", "email": "marketing@growthco.com", "source": "website"},
    {"name": "CEO", "company": "ScaleUp Ltd", "email": "ceo@scaleupltd.com", "source": "referral"},
    {"name": "Operations Head", "company": "EfficiencyPro", "email": "ops@efficiencypro.com", "source": "linkedin"},
    {"name": "Small Business Owner", "company": "LocalShop", "email": "owner@localshop.com", "source": "google_maps"},
]

PIPELINE_STAGES = ["lead", "contacted", "interested", "proposal", "negotiation", "closed_won", "closed_lost"]

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def generate_leads(count=3):
    """Generate new leads (in production, scrape real sources)"""
    leads = load_json(LEADS_FILE, {"leads": [], "campaigns": []})
    
    new_leads = []
    for i in range(count):
        template = random.choice(SAMPLE_LEADS)
        lead = {
            "id": f"lead_{int(time.time())}_{i}",
            "name": template["name"],
            "company": template["company"],
            "email": template["email"],
            "source": template["source"],
            "status": "new",
            "created_at": datetime.now().isoformat(),
            "last_contact": None,
            "clicked": False,
            "replied": False
        }
        new_leads.append(lead)
    
    leads["leads"].extend(new_leads)
    save_json(LEADS_FILE, leads)
    
    return new_leads

def send_outreach(lead):
    """Send cold email to lead"""
    # In production, integrate with email service
    email_template = f"""Hi {lead['name'].split()[0]},

I help companies automate their workflows and save 10+ hours per week.

Would love to show you how we're helping businesses like yours.

Best,
The EveryCompanyClaw Team
"""
    log(f"📧 Would send to {lead['email']}: {email_template[:50]}...")
    return {"sent": True, "clicked": random.random() < 0.3, "replied": random.random() < 0.1}

def add_to_pipeline(lead, stage="lead", value=0):
    """Add lead to sales pipeline"""
    pipeline = load_json(PIPELINE_FILE, {"deals": []})
    
    deal = {
        "id": f"deal_{lead['id']}",
        "lead_id": lead["id"],
        "name": lead["name"],
        "company": lead["company"],
        "email": lead["email"],
        "stage": stage,
        "value": value,
        "probability": 0.2,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "last_activity": "Added to pipeline"
    }
    
    # Check if already in pipeline
    existing = [d for d in pipeline["deals"] if d["lead_id"] == lead["id"]]
    if not existing:
        pipeline["deals"].append(deal)
        save_json(PIPELINE_FILE, pipeline)
        return deal
    
    return existing[0]

def move_stage(deal_id, new_stage):
    """Move deal to new pipeline stage"""
    pipeline = load_json(PIPELINE_FILE, {"deals": []})
    
    for deal in pipeline["deals"]:
        if deal["id"] == deal_id:
            deal["stage"] = new_stage
            deal["updated_at"] = datetime.now().isoformat()
            deal["last_activity"] = f"Moved to {new_stage}"
            
            # Update probability based on stage
            stage_probs = {"lead": 0.1, "contacted": 0.2, "interested": 0.4, "proposal": 0.6, "negotiation": 0.8, "closed_won": 1.0, "closed_lost": 0}
            deal["probability"] = stage_probs.get(new_stage, 0.2)
            
            # Random close for demo
            if new_stage == "closed_won":
                deal["value"] = random.randint(500, 5000)
    
    save_json(PIPELINE_FILE, pipeline)

def get_pipeline_summary():
    """Get pipeline summary"""
    pipeline = load_json(PIPELINE_FILE, {"deals": []})
    leads = load_json(LEADS_FILE, {"leads": []})
    
    stages = {}
    total_value = 0
    for deal in pipeline["deals"]:
        stage = deal["stage"]
        stages[stage] = stages.get(stage, 0) + 1
        total_value += deal.get("value", 0)
    
    return {
        "total_leads": len(leads["leads"]),
        "active_deals": len(pipeline["deals"]),
        "stages": stages,
        "total_value": total_value,
        "leads_clicked": sum(1 for l in leads["leads"] if l.get("clicked")),
        "leads_replied": sum(1 for l in leads["leads"] if l.get("replied"))
    }

def run_lead_gen():
    """Main lead gen workflow"""
    log("🎯 Starting Lead Generation...")
    
    # 1. Generate new leads
    new_leads = generate_leads(2)
    log(f"   Generated {len(new_leads)} new leads")
    
    # 2. Send outreach to first-time leads
    leads = load_json(LEADS_FILE, {"leads": []})
    outreach_sent = 0
    
    for lead in leads["leads"]:
        if lead["status"] == "new":
            result = send_outreach(lead)
            lead["status"] = "contacted"
            lead["last_contact"] = datetime.now().isoformat()
            lead["clicked"] = result.get("clicked", False)
            lead["replied"] = result.get("replied", False)
            outreach_sent += 1
            
            # Add to pipeline
            add_to_pipeline(lead, "contacted")
    
    save_json(LEADS_FILE, leads)
    log(f"   Sent {outreach_sent} outreach emails")
    
    # 3. Update pipeline (simulate progression)
    pipeline = load_json(PIPELINE_FILE, {"deals": []})
    for deal in pipeline["deals"][:2]:  # Move first 2 deals
        if deal["stage"] == "contacted" and random.random() < 0.3:
            move_stage(deal["id"], "interested")
            log(f"   {deal['company']} moved to 'interested'")
        elif deal["stage"] == "interested" and random.random() < 0.2:
            move_stage(deal["id"], "proposal")
            log(f"   {deal['company']} moved to 'proposal'")
    
    # 4. Summary
    summary = get_pipeline_summary()
    log(f"   Pipeline: {summary['active_deals']} deals, ${summary['total_value']} value")
    log(f"   Leads: {summary['leads_clicked']} clicked, {summary['leads_replied']} replied")
    
    return summary

if __name__ == "__main__":
    print("🎯 LEAD GEN + PIPELINE AGENT")
    print("="*40)
    
    summary = run_lead_gen()
    
    print(f"\n📊 PIPELINE SUMMARY:")
    print(f"   Total Leads: {summary['total_leads']}")
    print(f"   Active Deals: {summary['active_deals']}")
    print(f"   Total Value: ${summary['total_value']}")
    print(f"   Leads Clicked: {summary['leads_clicked']}")
    print(f"   Leads Replied: {summary['leads_replied']}")
    
    print(f"\n📍 PIPELINE STAGES:")
    for stage, count in summary['stages'].items():
        print(f"   {stage}: {count}")
    
    print("\n✅ Lead gen complete!")
