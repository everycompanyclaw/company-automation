#!/usr/bin/env python3
"""
Message Router
Routes messages to correct bot
"""

PERSONAL_BOT_TOKEN = "8677779317:AAEaxRQmEpymFeer0sVPXe1YNMUqcURZACg"
COMPANY_BOT_TOKEN = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"

def route_message(text, chat_id="96691420"):
    """Route message to correct bot"""
    text_lower = text.lower()
    
    # Company keywords
    company_keywords = ["company", "business", "leads", "sales", "build", 
                       "research", "client", "project", "customer", "service"]
    
    # Check if company-related
    if any(kw in text_lower for kw in company_keywords):
        # Send to company bot
        send_to_company(text, chat_id)
        return "company"
    else:
        # Handle personally
        return "personal"

def send_to_company(text, chat_id):
    """Forward to company bot"""
    # This would integrate with company bot handler
    print(f"Routing to company bot: {text}")

def send_to_personal(text, chat_id):
    """Send to personal bot"""
    # Already in personal chat
    pass

# Keywords for routing
ROUTE_RULES = {
    "company": ["company", "business", "leads", "sales", "build", "research", 
                "client", "project", "service", "automation", "customer"],
    "personal": ["personal", "me", "my", "home", "private"]
}

if __name__ == "__main__":
    # Test routing
    test_messages = [
        "Build a website for my company",
        "Find leads for business",
        "What's the weather",
        "Research AI trends",
        "Help me with personal stuff"
    ]
    
    print("Message Routing Test:\n")
    for msg in test_messages:
        result = route_message(msg)
        print(f"'{msg}' → {result}")
