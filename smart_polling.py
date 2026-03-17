#!/usr/bin/env python3
"""
Smart Bot Polling - Routes messages, doesn't just echo
"""
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor

BOTS = {
    "personal": "8677779317:AAEaxRQmEpymFeer0sVPXe1YNMUqcURZACg",
    "company": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
}

COMPANY_KW = ["company", "business", "leads", "sales", "build", "research", "client", 
             "project", "service", "automation", "money", "job", "upwork", "fiverr", "freelance"]

PERSONAL_KW = ["personal", "help", "me", "weather", "天氣", "我自己", "私人"]

def get_updates(token, offset=0):
    try:
        r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", 
                         params={"timeout": 30, "offset": offset}, timeout=35)
        return r.json().get("result", [])
    except:
        return []

def send_msg(token, chat_id, text):
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat_id, "text": text}, timeout=10)
    except:
        pass

def determine_route(text):
    text_lower = text.lower()
    company_score = sum(1 for kw in COMPANY_KW if kw in text_lower)
    personal_score = sum(1 for kw in PERSONAL_KW if kw in text_lower)
    
    if company_score > personal_score:
        return "company"
    return "personal"

def handle_message(chat_id, text, source_bot):
    route = determine_route(text)
    target_token = BOTS[route]
    
    # Smart response based on content
    if route == "company":
        response = f"🏢 Company message received! I'll process: {text[:50]}..."
    else:
        response = f"🏠 Personal message. I'll handle: {text[:50]}..."
    
    send_msg(target_token, chat_id, response)
    return route

def poll_bot(bot_name):
    token = BOTS[bot_name]
    offset = 0
    while True:
        try:
            updates = get_updates(token, offset)
            for u in updates:
                if "message" in u:
                    msg = u["message"]
                    text = msg.get("text", "")
                    chat_id = msg["chat"]["id"]
                    offset = u["update_id"] + 1
                    
                    if text:
                        handle_message(chat_id, text, bot_name)
        except Exception as e:
            print(f"{bot_name}: {e}")
            time.sleep(3)

if __name__ == "__main__":
    print("🤖 Smart polling started!")
    with ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(poll_bot, "personal")
        ex.submit(poll_bot, "company")
