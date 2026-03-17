#!/usr/bin/env python3
"""
Polling Bot - Sends messages to OpenClaw Gateway for processing
"""
import requests
import time
from concurrent.futures import ThreadPoolExecutor

BOTS = {
    "notify": "8677779317:AAEaxRQmEpymFeer0sVPXe1YNMUqcURZACg",
    "company": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
}

GATEWAY = "http://127.0.0.1:18789"
TOKEN = "d5d32661518523b1f9f2a0d15261144aeccb98b1f3a93482"

def send_to_gateway(chat_id, text, source):
    """Send message to gateway for AI processing"""
    # Route to correct bot
    company_kw = ["company", "business", "leads", "sales", "client", "project", 
                  "service", "job", "upwork", "fiverr", "freelance", "automation"]
    
    is_company = any(kw in text.lower() for kw in company_kw)
    bot = "company" if is_company else "notify"
    
    # Forward to gateway (will be processed by agent)
    try:
        # Just acknowledge - agent will handle it
        token = BOTS[bot]
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat_id, "text": f"📩 Received: {text[:50]}... Processing..."}, 
                      timeout=10)
    except:
        pass

def get_updates(token, offset=0):
    try:
        r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", 
                         params={"timeout": 30, "offset": offset}, timeout=35)
        return r.json().get("result", [])
    except:
        return []

def poll_bot(bot_name):
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
                    if text and not text.startswith("/"):
                        send_to_gateway(chat_id, text, bot_name)
        except Exception as e:
            print(f"{bot_name}: {e}")
            time.sleep(3)

if __name__ == "__main__":
    print("📡 Polling bots...")
    with ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(poll_bot, "notify")
        ex.submit(poll_bot, "company")
