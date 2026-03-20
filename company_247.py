#!/usr/bin/env python3
"""
24/7 Company Runner
Reports actual company operations
"""
import os
import time
import requests
import subprocess
import json
from datetime import datetime

COMPANY_BOT = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
STATE_FILE = "/tmp/learn_state.json"

def send_msg(text):
    """Send update to Telegram"""
    try:
        requests.post(f"https://api.telegram.org/bot{COMPANY_BOT}/sendMessage",
                      json={"chat_id": "96691420", "text": text}, timeout=10)
    except:
        pass

def get_company_status():
    """Get what company is doing"""
    try:
        # Read learning state
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
        
        topics = state.get("topics_done", [])
        actions = state.get("actions_done", [])
        
        if topics:
            return f"🧠 Learning: {topics[-1]}"
        if actions:
            return f"⚡ Last action: {actions[-1]}"
    except:
        pass
    
    return "🏢 Company operating..."

def run_operations():
    """Run company operations"""
    try:
        result = subprocess.run(
            ["python3", "/Users/macbookpro/.openclaw/workspace/company/aggressive_learn.py"],
            capture_output=True, timeout=60
        )
        status = get_company_status()
        return status
    except Exception as e:
        return f"⚙️ Running: {e}"

def main():
    while True:
        # Run operations every cycle
        status = run_operations()
        
        # Only send if there's meaningful update
        if "Learning:" in status or "action:" in status:
            send_msg(f"🏢 {status}")
        else:
            print(status)
        
        # Sleep 5 minutes
        time.sleep(300)

if __name__ == "__main__":
    main()
