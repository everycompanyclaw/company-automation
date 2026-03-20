#!/usr/bin/env python3
"""
Live CRM Dashboard - Visualize what company is working on
Run this to see real-time company status
"""
import os
import json
from datetime import datetime

CRM_FILE = "/tmp/company_crm.json"
LEARN_STATE = "/tmp/learn_state.json"

def load_crm():
    if os.path.exists(CRM_FILE):
        with open(CRM_FILE, "r") as f:
            return json.load(f)
    return {"leads": [], "activities": [], "pipeline": [], "tasks": []}

def show_dashboard():
    """Display live dashboard"""
    crm = load_crm()
    
    # Load learning state
    learn_state = {"topics_done": [], "actions_done": []}
    if os.path.exists(LEARN_STATE):
        with open(LEARN_STATE, "r") as f:
            learn_state = json.load(f)
    
    topics = learn_state.get("topics_done", [])
    actions = learn_state.get("actions_done", [])
    
    print("=" * 60)
    print("🏢 EVERYCOMPANYCLAW - LIVE CRM DASHBOARD")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Current Focus
    print("🎯 CURRENT FOCUS")
    print("-" * 40)
    if topics:
        print(f"   Learning: {topics[-1]}")
    if actions:
        print(f"   Doing: {actions[-1]}")
    print()
    
    # Pipeline
    print("🔻 SALES PIPELINE")
    print("-" * 40)
    if crm.get("pipeline"):
        for p in crm["pipeline"][-5:]:
            print(f"   [{p['stage']}] {p['item']}")
    else:
        print("   (empty)")
    print()
    
    # Leads
    print("👥 LEADS")
    print("-" * 40)
    print(f"   Total: {len(crm.get('leads', []))}")
    if crm.get("leads"):
        for lead in crm["leads"][-5:]:
            print(f"   • {lead['name']} ({lead['source']}) - {lead['status']}")
    print()
    
    # Recent Activities
    print("⚡ RECENT ACTIVITIES")
    print("-" * 40)
    activities = crm.get("activities", [])[-10:]
    if activities:
        for a in activities:
            print(f"   [{a['time'][-5:]}] {a['action']}: {a['details'][:40]}...")
    else:
        print("   No activities yet")
    print()
    
    # Stats
    print("📊 STATS")
    print("-" * 40)
    print(f"   Topics studied: {len(topics)}")
    print(f"   Actions done: {len(actions)}")
    print(f"   Leads: {len(crm.get('leads', []))}")
    print()
    
    print("=" * 60)

if __name__ == "__main__":
    show_dashboard()
