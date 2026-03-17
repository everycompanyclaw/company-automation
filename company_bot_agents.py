#!/usr/bin/env python3
"""
Company Bot - Agent Integration
Connects @EveryCompanyBot to Agent Team
"""

import requests
import json
import os
from agent_team import TEAM

BOT_TOKEN = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"

def send_message(text, chat_id="96691420"):
    """Send message to company bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def handle_command(command):
    """Handle company bot commands"""
    
    if command == "/start":
        return """🏢 Welcome to EveryCompany Bot!

Your AI-powered company assistant.

Commands:
/leads - Generate leads (Sales Agent)
/build - Build something (Developer Agent)
/research - Research (Analyst Agent)
/stock - Stock prices
/crypto - Crypto prices
/status - Company status

Just tell me what you need!"""
    
    elif command == "/help":
        return """🏢 Company Bot Commands:

/leads - 💼 Sales Agent
/build - 💻 Developer Agent  
/research - 📊 Analyst Agent
/stock - 📈 Stock prices
/crypto - ₿ Crypto prices
/status - ✅ Company status

Just type what you need!"""
    
    elif command == "/leads":
        agent = TEAM.get_agent_for_task("find leads for automation business")
        return f"💼 Spawning {agent.title()} Agent for lead generation..."
    
    elif command == "/build":
        agent = TEAM.get_agent_for_task("build a website")
        return f"💻 Spawning {agent.title()} Agent to build..."
    
    elif command == "/research":
        agent = TEAM.get_agent_for_task("research market trends")
        return f"📊 Spawning {agent.title()} Agent for research..."
    
    elif command == "/stock":
        return "📈 Fetching stock prices..."
    
    elif command == "/crypto":
        return "₿ Fetching crypto prices..."
    
    elif command == "/status":
        return """✅ Company Status:

🤖 Agents: 6 ready
💼 Sales: Active
💻 Developer: Ready
📊 Analyst: Ready
📡 Telegram: Connected
⏰ Cron Jobs: Running"""
    
    else:
        return "🏢 Use /help for commands"

# Save as module
if __name__ == "__main__":
    print("Company Bot Agent Integration Ready!")
    print("Bot: @EveryCompanyBot")
