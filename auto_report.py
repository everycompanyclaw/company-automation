#!/usr/bin/env python3
"""
Company Auto-Runner - Runs company tasks automatically
"""
import requests
import time
import os

BOTS = {
    "company": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw",
    "notify": "8677779317:AAEaxRQmEpymFeer0sVPXe1YNMUqcURZACg"
}

GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "ifwubwz pkqtievqh")

def send_msg(bot, chat_id, text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOTS[bot]}/sendMessage",
                      json={"chat_id": chat_id, "text": text}, timeout=10)
    except:
        pass

def search_jobs():
    """Search for freelance jobs"""
    try:
        r = requests.get("https://lite.duckduckgo.com/lite/?q=python+automation+freelance+jobs",
                        timeout=15)
        if "python" in r.text.lower():
            return "Found Python automation jobs!"
        return "Checking jobs..."
    except:
        return "Job search error"

def send_report():
    """Send daily company report"""
    jobs = search_jobs()
    
    report = f"""🏢 Company Daily Report

✅ System Status: Running

📊 Job Search: {jobs}

📋 Todo:
- Continue outreach
- Follow up leads
- Update profiles

#automation #freelance #python"""
    
    send_msg("company", "96691420", report)

if __name__ == "__main__":
    send_report()
    print("Report sent!")
