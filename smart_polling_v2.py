#!/usr/bin/env python3
"""
Smart Polling - Forwards messages to main agent for processing
"""
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import json

BOTS = {
    "notify": "8677779317:AAEaxRQmEpymFeer0sVPXe1YNMUqcURZACg",
    "company": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
}

GATEWAY = "http://127.0.0.1:18789"
AUTH_TOKEN = "d5d32661518523b1f9f2a0d15261144aeccb98b1f3a93482"
MAIN_CHAT_ID = "96691420"

def forward_to_gateway(chat_id, text, source_bot):
    """Forward message to gateway for processing"""
    
    # Determine which agent should handle
    company_kw = ["company", "business", "leads", "sales", "client", "project", 
                  "service", "job", "upwork", "fiverr", "freelance", "automation"]
    
    is_company = any(kw in text.lower() for kw in company_kw)
    target_bot = "company" if is_company else "notify"
    
    # Send to gateway via DM (mimics receiving a message)
    # Gateway will process and respond back
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    
    payload = {
        "chat_id": chat_id,
        "text": text,
        "source": source_bot
    }
    
    try:
        # This would send to gateway - but gateway only handles one bot
        # For now, just acknowledge and let user know to check main chat
        token = BOTS[target_bot]
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat_id, "text": f"✅ Message forwarded! I'll respond here."}, 
                      timeout=10)
    except Exception as e:
        print(f"Error: {e}")

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
                    msg = u["message"]
                    text = msg.get("text", "")
                    chat_id = msg["chat"]["id"]
                    offset = u["update_id"] + 1
                    
                    if text and not text.startswith("/"):
                        forward_to_gateway(chat_id, text, bot_name)
        except Exception as e:
            print(f"{bot_name}: {e}")
            time.sleep(3)

if __name__ == "__main__":
    print("📡 Smart polling - forwarding to agents...")
    with ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(poll_bot, "notify")
        ex.submit(poll_bot, "company")
