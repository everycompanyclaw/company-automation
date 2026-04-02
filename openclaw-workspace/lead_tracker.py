#!/usr/bin/env python3
"""Lead & Pipeline Tracker CLI for EveryCompanyClaw HQ"""

import json
import sys
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_FILE = os.path.join(BASE_DIR, "leads.json")
PIPELINE_FILE = os.path.join(BASE_DIR, "pipeline.json")

def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def add_lead(email, source):
    data = load_json(LEADS_FILE, {"leads": [], "last_updated": None})
    lead = {
        "email": email,
        "source": source,
        "created": datetime.utcnow().isoformat() + "Z",
        "status": "new"
    }
    data["leads"].append(lead)
    data["last_updated"] = datetime.utcnow().isoformat() + "Z"
    save_json(LEADS_FILE, data)
    print(f"✅ Lead added: {email} (source: {source})")
    print(f"   Total leads: {len(data['leads'])}")

def add_deal(company, value):
    data = load_json(PIPELINE_FILE, {"deals": [], "last_updated": None})
    deal = {
        "company": company,
        "value": float(value),
        "stage": "prospecting",
        "created": datetime.utcnow().isoformat() + "Z"
    }
    data["deals"].append(deal)
    data["last_updated"] = datetime.utcnow().isoformat() + "Z"
    save_json(PIPELINE_FILE, data)
    total = sum(d["value"] for d in data["deals"])
    print(f"✅ Deal added: {company} — ${value}")
    print(f"   Total pipeline: ${total:.2f}")

def status():
    leads_data = load_json(LEADS_FILE, {"leads": [], "last_updated": None})
    pipeline_data = load_json(PIPELINE_FILE, {"deals": [], "last_updated": None})
    total_pipeline = sum(d["value"] for d in pipeline_data["deals"])

    print("=" * 40)
    print("  EVERYCOMPANYCLAW HQ — STATUS REPORT")
    print("=" * 40)
    print(f"  📋 Leads:        {len(leads_data['leads'])}")
    print(f"  💰 Pipeline:     ${total_pipeline:,.2f}")
    print(f"  📊 Deals:        {len(pipeline_data['deals'])}")
    print("-" * 40)
    if leads_data["last_updated"]:
        print(f"  Leads updated:   {leads_data['last_updated']}")
    if pipeline_data["last_updated"]:
        print(f"  Pipeline updated: {pipeline_data['last_updated']}")
    print("=" * 40)

def list_leads():
    data = load_json(LEADS_FILE, {"leads": [], "last_updated": None})
    if not data["leads"]:
        print("No leads yet.")
        return
    for i, lead in enumerate(data["leads"], 1):
        print(f"  {i}. {lead['email']} [{lead.get('source','?')}] — {lead.get('status','?')}")

def list_deals():
    data = load_json(PIPELINE_FILE, {"deals": [], "last_updated": None})
    if not data["deals"]:
        print("No deals yet.")
        return
    for i, deal in enumerate(data["deals"], 1):
        print(f"  {i}. {deal['company']} — ${deal['value']:.2f} [{deal.get('stage','?')}]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lead_tracker.py <command> [args]")
        print("  add-lead   <email> <source>")
        print("  add-deal   <company> <value>")
        print("  status")
        print("  list-leads")
        print("  list-deals")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "add-lead":
        if len(sys.argv) < 4:
            print("Usage: lead_tracker.py add-lead <email> <source>")
            sys.exit(1)
        add_lead(sys.argv[2], sys.argv[3])
    elif cmd == "add-deal":
        if len(sys.argv) < 4:
            print("Usage: lead_tracker.py add-deal <company> <value>")
            sys.exit(1)
        add_deal(sys.argv[2], sys.argv[3])
    elif cmd == "status":
        status()
    elif cmd == "list-leads":
        list_leads()
    elif cmd == "list-deals":
        list_deals()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
