#!/usr/bin/env python3
"""
Daily Report to Company Bot - All in one
"""
import os
from datetime import datetime

COMPANY_BOT = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
CHAT_ID = "96691420"

def send_report():
    """Send daily report to CompanyBot"""
    import requests
    
    report = f"""
📊 EveryCompany - Daily Report
===========================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

⚡ Status: Running
🤖 Agents: Active
📱 Automation: Running

---
Run: company_bot_agent.py
"""
    
    url = f"https://api.telegram.org/bot{COMPANY_BOT}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": report}
    requests.post(url, data=data)
    print("Report sent to CompanyBot!")

if __name__ == "__main__":
    send_report()
