#!/usr/bin/env python3
"""
Simple Bot Polling - Real-time message handling
"""
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Bot tokens  
BOTS = {
    "personal": os.environ.get("PERSONAL_BOT_TOKEN", "8677779317:AAEaxRQmEpymFeer0sVPXe1YNMUqcURZACg"),
    "company": os.environ.get("COMPANY_BOT_TOKEN", "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw")
}

COMPANY_KW = ["company", "business", "leads", "sales", "build", "research", "client", "project", "service", "automation", "money", "job", "upwork", "fiverr"]

def get_updates(bot_name, offset=0):
    token = BOTS[bot_name]
    r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", 
                     params={"timeout": 60, "offset": offset}, timeout=65)
    return r.json().get("result", [])

def send(bot_name, chat_id, text):
    token = BOTS[bot_name]
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                  json={"chat_id": chat_id, "text": text})

def process_update(bot_name, update):
    if "message" not in update: return
    msg = update["message"]
    text = msg.get("text", "")
    chat_id = msg["chat"]["id"]
    offset = update["update_id"]
    
    # Route
    is_company = any(kw in text.lower() for kw in COMPANY_KW)
    target = "company" if is_company else "personal"
    target_bot = BOTS[target]
    
    # Echo
    prefix = "🏢" if is_company else "🏠"
    send(target, chat_id, f"{prefix} Got: {text}")
    
    return offset

def poll_bot(bot_name):
    offset = 0
    while True:
        try:
            updates = get_updates(bot_name, offset)
            for u in updates:
                new_offset = process_update(bot_name, u)
                if new_offset: offset = new_offset + 1
        except Exception as e:
            print(f"Error {bot_name}: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("🤖 Starting bots...")
    with ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(poll_bot, "personal")
        ex.submit(poll_bot, "company")
