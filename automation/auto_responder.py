#!/usr/bin/env python3
"""
Auto-Responder Bot - Ready-to-use automation product
Handles common inquiries automatically
"""
import json
import os
from datetime import datetime

CONFIG_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/auto_responder_config.json"
LOG_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/responses.log"

# Knowledge base
KB = {
    "price": """Our services:
- Workflow Automation: $500-1,500
- AI Integration: $1,500-4,000  
- Custom Software: $2,000-8,000
- Monthly Retainer: $500-2,000/month

Free 15-min consultation included!""",

    "timeline": """Typical timelines:
- Simple automation: 1-2 weeks
- AI integration: 2-4 weeks
- Custom software: 4-8 weeks

We work fast!""",

    "process": """Our process:
1. Free discovery call (15 min)
2. Proposal within 24 hours
3. 50% deposit to start
4. Build & iterate
5. Final payment on delivery
6. 2 weeks support included""",

    "contact": """Email: everycompanyclaw@gmail.com
Response time: Within 24 hours""",

    "services": """We specialize in:
🔄 Workflow automation (Zapier, Make, n8n)
🤖 AI chatbots & assistants
💻 Python scripts & APIs
📊 Data processing & reporting
🔗 API integrations"""
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"keywords": {}, "responses": {}}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def match_intent(message):
    """Simple keyword matching for intent"""
    msg = message.lower()
    
    keywords = {
        "price": ["price", "cost", "cost", "how much", "pricing", "fee"],
        "timeline": ["timeline", "how long", "when", "duration", "weeks"],
        "process": ["process", "how does it work", "steps", "how do you"],
        "contact": ["contact", "reach", "email", "phone", "whatsapp"],
        "services": ["services", "what do you do", "offer", "specialize"]
    }
    
    for intent, words in keywords.items():
        if any(w in msg for w in words):
            return intent
    return None

def respond(message):
    """Generate response"""
    intent = match_intent(message)
    
    if intent:
        response = KB.get(intent, "Thanks for reaching out!")
        log_response(message, response, intent)
        return response
    
    # Default response
    default = """Thanks for your message! For a quick answer, ask me about:
- Services we offer
- Pricing
- Timeline
- Our process

Or email directly: everycompanyclaw@gmail.com"""
    
    log_response(message, default, "default")
    return default

def log_response(query, response, intent):
    """Log the interaction"""
    entry = f"[{datetime.now().isoformat()}] {intent}: {query[:50]}...\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)

# CLI for testing
if __name__ == "__main__":
    print("🤖 Auto-Responder Bot")
    print("Type 'quit' to exit\n")
    
    while True:
        msg = input("You: ")
        if msg.lower() in ['quit', 'exit']:
            break
        print(f"\nBot: {respond(msg)}\n")
