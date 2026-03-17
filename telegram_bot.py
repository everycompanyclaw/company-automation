#!/usr/bin/env python3
"""
Telegram Bot - General Purpose
Handles all types of requests
"""

import os
import json
import requests
from datetime import datetime

# Load credentials
CREDS = json.load(open("/Users/macbookpro/.config/income-automation.json"))
BOT_TOKEN = CREDS["bot_token"]
CHAT_ID = CREDS["chat_id"]

# Command handlers
COMMANDS = {
    "/start": "Welcome! I'm your AI assistant. Ask me anything!",
    "/help": "Commands:\n/start - Welcome\n/agent - Spawn agent\n/stock - Stock prices\n/weather - Weather\n/earnings - Earnings calendar",
    "/agent": "Tell me what you need - I'll spawn the right agent!",
    "/stock": "Fetching stock prices...",
    "/weather": "Fetching weather...",
    "/earnings": "Getting earnings calendar...",
}

def send_message(text, chat_id=CHAT_ID):
    """Send Telegram message"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def handle_message(text):
    """Handle incoming message"""
    text = text.strip()
    
    # Check commands
    if text in COMMANDS:
        return COMMANDS[text]
    
    # Default: analyze and respond
    return f"I'll help with that! Processing..."

def main():
    """Main bot loop"""
    print("🤖 General Purpose Bot Started")
    print(f"Bot: @NotifyClawBot")
    print(f"Chat ID: {CHAT_ID}")
    
    # Get updates
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    r = requests.get(url)
    print(f"Updates: {len(r.json().get('result', []))}")
    
    print("\nBot is running! Send a message...")

if __name__ == "__main__":
    main()
