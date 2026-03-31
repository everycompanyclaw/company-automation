#!/usr/bin/env python3
"""
Daily Evening Report — sends to MK via Telegram
"""
import requests
import json
import os
from datetime import datetime

TOKEN = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
CHAT_ID = "96691420"

def send_telegram(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
            timeout=15
        )
        return True
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def get_stats():
    stats = {}
    try:
        with open("/tmp/company-automation/stats.json") as f:
            stats = json.load(f)
    except:
        pass
    return stats

def main():
    stats = get_stats()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    msg = f"""🏢 *EveryCompanyClaw — Evening Report*
━━━━━━━━━━━━━━━━━━

📅 {now}

📊 *Today's Stats*
   Leads: {stats.get('leads_generated', '?')}
   Pipeline Deals: {stats.get('pipeline_deals', '?')}
   Actions: {stats.get('actions_completed', '?')}
   Social Posts: {stats.get('social_posts', '?')}

📋 *Pipeline Status*
   Running: ✅

🌐 *Links*
   Website: everycompanyclaw.github.io
   GitHub: github.com/everycompanyclaw

━━━━━━━━━━━━━━━━━━
_Report auto-generated_"""

    if send_telegram(msg):
        print(f"✅ Report sent at {now}")
    else:
        print(f"❌ Failed to send report")

if __name__ == "__main__":
    main()
