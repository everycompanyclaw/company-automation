#!/usr/bin/env python3
"""
Company Auto-Runner - Detailed profit-focused reports
"""
import requests
import os
import json
from datetime import datetime

BOTS = {
    "company": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw",
    "notify": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
}

def send_msg(bot, chat_id, text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOTS[bot]}/sendMessage",
                      json={"chat_id": chat_id, "text": text}, timeout=10)
    except:
        pass

def get_company_status():
    """Get detailed company status"""
    try:
        with open("/tmp/learn_state.json", "r") as f:
            state = json.load(f)
        
        topics = state.get("topics_done", [])
        actions = state.get("actions_done", [])
        
        # Get last 5 topics and actions
        recent_topics = topics[-5:] if topics else []
        recent_actions = actions[-5:] if actions else []
        
        report = f"""
🧠 LEARNING ({len(topics)} total)
"""
        for t in recent_topics:
            report += f"   • {t}\n"
        
        report += f"""
⚡ ACTIONS ({len(actions)} total)
"""
        for a in recent_actions:
            report += f"   • {a}\n"
        
        return report, topics[-1] if topics else "None", len(topics), len(actions)
    except Exception as e:
        return f"\n⚠️ Error: {e}\n", "Error", 0, 0

def send_report():
    """Send detailed daily company report"""
    details, last_topic, topics_count, actions_count = get_company_status()
    
    report = f"""🏢 EVERYCOMPANYCLAW - DAILY REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}

✅ STATUS: Running

💰 FOCUS: Revenue & Profit

📊 STATS
   Topics Studied: {topics_count}
   Actions Done: {actions_count}
   Last Topic: {last_topic}

{details}
📋 TODAY'S PRIORITIES
   • Generate leads
   • Cold outreach
   • Create offers
   • Follow up prospects

🌐 LINKS
   Website: everycompanyclaw.github.io/company-automation/
   Products: Python Scripts $79 | Zapier $49 | AI Prompts $29

━━━━━━━━━━━━━━━━━━━━━━━━━━━
#AI #Automation #Business
"""
    
    send_msg("company", "96691420", report)

if __name__ == "__main__":
    send_report()
    print("Detailed report sent!")
