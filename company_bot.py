#!/usr/bin/env python3
"""
Company Bot Handler - @EveryCompanyBot
Separate from personal bot
"""

import json

COMPANY_BOT_TOKEN = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"

# Company-specific commands
COMMANDS = {
    "/start": "🏢 Welcome to EveryCompany Bot!\n\nYour company automation assistant.\n\nCommands:\n/leads - Generate leads\n/build - Build something\n/research - Research\n/stock - Stock prices\n/crypto - Crypto\n/status - Company status",
    
    "/help": """🏢 Company Bot Commands:

/leads - Lead generation
/build - Development/building
/research - Research & analysis
/stock - Stock prices  
/crypto - Crypto prices
/status - Company status

This bot handles company operations!""",
    
    "/leads": "💼 Lead generation system - Running...",
    "/build": "💻 Development system - Ready",
    "/research": "📊 Research system - Ready",
    "/stock": "📈 Fetching stocks...",
    "/crypto": "₿ Fetching crypto...",
    "/status": "✅ Company systems operational"
}

def handle_company_message(text):
    """Handle company bot messages"""
    return COMMANDS.get(text, "🏢 Use /help for commands")

# Save company bot config
print("Company bot configured!")
print(f"Bot: @EveryCompanyBot")
print(f"Token: {COMPANY_BOT_TOKEN[:20]}...")
