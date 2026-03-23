#!/usr/bin/env python3
"""
Simple Telegram Bot Polling
Runs in background and processes messages
"""

import requests
import json
import time
from datetime import datetime

# Bot tokens
BOTS = {
    "personal": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw",
    "company": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
}

# Keywords for routing
COMPANY_KEYWORDS = ["company", "business", "leads", "sales", "build", "research", 
                    "client", "project", "service", "automation", "money", "job"]

PERSONAL_KEYWORDS = ["personal", "help", "me", "weather", "天氣"]

def get_updates(bot_token, offset=0):
    """Get bot updates"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    params = {"timeout": 60, "offset": offset}
    try:
        r = requests.get(url, params=params, timeout=65)
        return r.json()
    except Exception as e:
        print(f"Error: {e}")
        return {"result": []}

def route_message(text):
    """Route to correct bot"""
    text_lower = text.lower()
    if any(kw in text_lower for kw in COMPANY_KEYWORDS):
        return "company"
    return "personal"

def send_message(bot_token, chat_id, text):
    """DISABLED - User requested no messages"""
    return  # Disabled
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def main():
    """Main polling loop"""
    print("🤖 Bot Polling Started...")
    print("Personal: @NotifyClawBot")
    print("Company: @EveryCompanyBot")
    
    offset = 0
    
    while True:
        updates = get_updates(BOTS["personal"], offset)
        
        if updates.get("result"):
            for update in updates["result"]:
                offset = update["update_id"] + 1
                
                if "message" in update:
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    text = msg.get("text", "")
                    
                    # Route message
                    bot = route_message(text)
                    token = BOTS[bot]
                    
                    # Echo with bot indicator
                    indicator = "🏢" if bot == "company" else "🏠"
                    send_message(token, chat_id, f"{indicator} Received: {text}")
                    
                    print(f"Message routed to {bot}: {text[:30]}...")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
