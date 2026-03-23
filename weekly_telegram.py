#!/usr/bin/env python3
"""
WEEKLY REPORT - Sends to Telegram Notify Bot
"""
import os
import json
import requests
from datetime import datetime

# Telegram Notify Bot
TELEGRAM_TOKEN = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
CHAT_ID = "96691420"

def get_stats():
    """Get company statistics"""
    state = {"topics_done": [], "actions_done": []}
    try:
        with open("/tmp/learn_state.json", "r") as f:
            state = json.load(f)
    except:
        pass
    
    return {
        "topics": len(state.get("topics_done", [])),
        "actions": len(state.get("actions_done", [])),
    }

def send_telegram(message):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, json=data, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def send_weekly_report():
    """Generate and send weekly report"""
    stats = get_stats()
    
    report = f"""
📊 <b>EveryCompanyClaw - Weekly Report</b>
━━━━━━━━━━━━━━━━━━━━━━

🧠 <b>Learning</b>
• Topics Explored: {stats['topics']}
• Actions Done: {stats['actions']}

💰 <b>Products</b>
• Python Scripts: $79
• Zapier Templates: $49
• AI Prompts: $29

🌐 <b>Website</b>
• everycompanyclaw.github.io/company-automation/

⚡ <b>Status</b>
• Self-learning: ✅ Every 3 min
• Operations: ✅ 24/7

⚠️ <b>Challenges</b>
• Instagram: Manual click
• Buffer: Need new token

📅 <b>Goals</b>
• First customer
• More exposure
• Product Hunt

━━━━━━━━━━━━━━
🟢 Company Operating
"""
    
    result = send_telegram(report)
    print(report)
    print("\nResult:", result)

if __name__ == "__main__":
    send_weekly_report()
