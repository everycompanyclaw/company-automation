#!/usr/bin/env python3
"""
Final Bot Routing System
- NotifyBot = Only Notifications
- CompanyBot = Company/Business
"""
import requests
import time
from concurrent.futures import ThreadPoolExecutor

BOTS = {
    "notify": "8677779317:AAEaxRQmEpymFeer0sVPXe1YNMUqcURZACg",
    "company": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
}

# Company goes to CompanyBot
COMPANY_KW = ["company", "business", "leads", "sales", "client", "project", 
             "service", "job", "upwork", "fiverr", "freelance", "automation",
             "build", "code", "develop", "create"]

# Only NOTIFICATIONS go to NotifyBot
NOTIFY_KW = ["stock", "crypto", "price", "weather", "alert", "earning", 
             "report", "notification", "reminder", "schedule"]

def determine_bot(text):
    text_lower = text.lower()
    
    # Company keywords → CompanyBot
    company_score = sum(1 for kw in COMPANY_KW if kw in text_lower)
    
    # Notify keywords → NotifyBot  
    notify_score = sum(1 for kw in NOTIFY_KW if kw in text_lower)
    
    if company_score > 0:
        return "company"
    elif notify_score > 0:
        return "notify"
    else:
        return "notify"  # Default to notify for now

def send(bot_name, chat_id, text):
    token = BOTS[bot_name]
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat_id, "text": text}, timeout=10)
    except:
        pass

def get_updates(token, offset=0):
    try:
        r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", 
                         params={"timeout": 30, "offset": offset}, timeout=35)
        return r.json().get("result", [])
    except:
        return []

def process(chat_id, text, source):
    bot = determine_bot(text)
    
    if bot == "company":
        msg = f"🏢 Company: {text[:50]}..."
    else:
        msg = f"📢 Notify: {text[:50]}..."
    
    send(bot, chat_id, msg)

def poll(bot_name):
    token = BOTS[bot_name]
    offset = 0
    while True:
        try:
            updates = get_updates(token, offset)
            for u in updates:
                if "message" in u:
                    text = u["message"].get("text", "")
                    chat_id = u["message"]["chat"]["id"]
                    offset = u["update_id"] + 1
                    if text:
                        process(chat_id, text, bot_name)
        except:
            time.sleep(3)

if __name__ == "__main__":
    print("🔔 NotifyBot = Notifications only!")
    print("🏢 CompanyBot = Business tasks!")
    with ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(poll, "notify")
        ex.submit(poll, "company")
