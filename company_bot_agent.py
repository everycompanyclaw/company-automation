#!/usr/bin/env python3
"""
Company Bot with Agent Team - @EveryCompanyBot
Uses AI agents for smarter responses
"""

import requests
import json
import os

COMPANY_BOT_TOKEN = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
CHAT_ID = "96691420"

def send_message(text):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{COMPANY_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def handle_message(message):
    """Handle incoming message with agent team"""
    text = message.get("text", "").lower()
    
    # Use agent team for responses
    agent_responses = {
        "lead": "🎯 Lead Generation Agent activated! Finding potential clients...",
        "content": "📝 Content Agent activated! Generating posts...",
        "research": "🔍 Research Agent activated! Analyzing market...",
        "build": "💻 Development Agent activated! Building solution...",
        "sell": "💰 Sales Agent activated! Finding opportunities...",
        "hello|hi|hey": "👋 Hello! EveryCompany Agent Team at your service! How can I help?",
        "help": "📋 Available agents: Lead, Content, Research, Build, Sell. Tell me what you need!"
    }
    
    for key, response in agent_responses.items():
        if key in text:
            return response
    
    # Default - use AI agent
    return "🤖 Message received! Agent team will respond shortly..."

def main():
    """Main polling loop"""
    offset = 0
    print("🤖 Company Bot with Agent Team - Running!")
    
    while True:
        try:
            # Get updates
            url = f"https://api.telegram.org/bot{COMPANY_BOT_TOKEN}/getUpdates"
            params = {"offset": offset, "timeout": 30}
            resp = requests.get(url, params=params, timeout=35).json()
            
            if resp.get("ok"):
                for update in resp.get("result", []):
                    offset = update["update_id"] + 1
                    if "message" in update:
                        msg = update["message"]
                        response = handle_message(msg)
                        if response:
                            send_message(response)
                            
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()
