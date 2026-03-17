#!/usr/bin/env python3
"""
Auto-Routing Bot System
- Claude Code for complex tasks
- MiniMax for simple tasks
- Route to correct bot
"""
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor

BOTS = {
    "notify": "8677779317:AAEaxRQmEpymFeer0sVPXe1YNMUqcURZACg",
    "company": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
}

# Keywords to determine complexity and routing
COMPLEX_KEYWORDS = ["build", "code", "program", "develop", "create", "analyze", "research", 
                    "strategy", "plan", "system", "automate", "script", "learn",
                    "complex", "deep", "detailed"]

COMPANY_KEYWORDS = ["company", "business", "leads", "sales", "client", "project", 
                   "service", "job", "upwork", "fiverr", "freelance", "automation"]

def determine_model_complexity(text):
    """Auto-select: Claude Code (Opus) vs MiniMax"""
    text_lower = text.lower()
    complex_score = sum(1 for kw in COMPLEX_KEYWORDS if kw in text_lower)
    
    if complex_score >= 2:
        return "claude_code"  # Use Opus
    return "minimax"  # Use MiniMax

def determine_routing(text):
    """Route to correct bot"""
    text_lower = text.lower()
    
    company_score = sum(1 for kw in COMPANY_KEYWORDS if kw in text_lower)
    
    if company_score > 0:
        return "company"
    return "notify"

def send_msg(bot_name, chat_id, text):
    token = BOTS[bot_name]
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat_id, "text": text}, timeout=10)
    except:
        pass

def process_message(chat_id, text, source_bot):
    """Process message: determine complexity + route"""
    
    # Determine complexity
    model = determine_model_complexity(text)
    
    # Determine routing
    route = determine_routing(text)
    
    # Build response
    if model == "claude_code":
        response = f"🤖 Complex task detected. Using Claude Code (Opus). Processing: {text[:30]}..."
    else:
        response = f"✅ Simple task. Using MiniMax. Processing: {text[:30]}..."
    
    # Send to correct bot
    target_bot = BOTS[route]
    send_msg(route, chat_id, response)
    
    return model, route

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
                        process_message(chat_id, text, bot_name)
        except Exception as e:
            print(f"{bot_name}: {e}")
            time.sleep(3)

if __name__ == "__main__":
    print("🤖 Auto-Routing System Started!")
    print("- Complex → Claude Code (Opus)")
    print("- Simple → MiniMax")
    print("- Company → @EveryCompanyBot")
    print("- Notify → @NotifyClawBot")
    
    with ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(poll_bot, "notify")
        ex.submit(poll_bot, "company")
