#!/usr/bin/env python3
"""
Live CRM Dashboard - Send to Telegram
"""
import os
import json
import requests
from datetime import datetime

CRM_FILE = "/tmp/company_crm.json"
LEARN_STATE = "/tmp/learn_state.json"

BOTS = {
    "company": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
}

def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOTS['company']}/sendMessage",
                      json={"chat_id": "96691420", "text": text, "parse_mode": "HTML"}, timeout=10)
    except:
        pass

def get_dashboard_text():
    """Generate dashboard text"""
    crm = {"leads": [], "activities": [], "pipeline": [], "tasks": []}
    if os.path.exists(CRM_FILE):
        with open(CRM_FILE, "r") as f:
            crm = json.load(f)
    
    learn_state = {"topics_done": [], "actions_done": []}
    if os.path.exists(LEARN_STATE):
        with open(LEARN_STATE, "r") as f:
            learn_state = json.load(f)
    
    topics = learn_state.get("topics_done", [])
    actions = learn_state.get("actions_done", [])
    
    text = f"""🏢 <b>LIVE COMPANY STATUS</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}

🎯 <b>CURRENT FOCUS</b>
   Learning: {topics[-1] if topics else 'None'}
   Doing: {actions[-1] if actions else 'None'}

📊 <b>STATS</b>
   Topics: {len(topics)}
   Actions: {len(actions)}
   Leads: {len(crm.get('leads', []))}

⚡ <b>LAST 5 ACTIVITIES</b>
"""
    
    for a in crm.get("activities", [])[-5:]:
        text += f"   [{a['time'][-5:]}] {a['action']}: {a['details'][:30]}...\n"
    
    if not crm.get("activities"):
        text += "   (none yet)\n"
    
    text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━
#EveryCompanyClaw #LiveDashboard
"""
    return text

if __name__ == "__main__":
    msg = get_dashboard_text()
    print(msg)
    send_msg(msg)
    print("\n✅ Dashboard sent to Telegram!")
