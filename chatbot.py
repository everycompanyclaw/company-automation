#!/usr/bin/env python3
"""
AI Chatbot for Website - Auto-respond to visitors
"""
import json
import random
from datetime import datetime

# Q&A Database
QA_PAIRS = {
    "hello|hi|hey": ["Hello! How can I help you today?", "Hi there! What can I do for you?", "Hey! Need help with automation?"],
    "service|services|你做啲咩": [
        "We offer: AI Automation, Web Development, Marketing Automation!",
        "我地既服務包括: AI自動化、網站開發、Marketing自動化!"
    ],
    "price|cost|幾多錢|收費": [
        "Prices start from $500 HKD. DM for details!",
        "收費由$500起，DM我傾下!"
    ],
    "contact|聯絡|contact": [
        "Email: everycompanyclaw@gmail.com",
        "Telegram: @EveryCompanyBot"
    ],
    "default": [
        "Thanks for your message! We'll get back to you soon.",
        "收到! 我地會盡快回覆你!"
    ]
}

def get_response(user_input):
    """Get AI response"""
    user_input = user_input.lower()
    for key, responses in QA_PAIRS.items():
        if any(k in user_input for k in key.split("|")):
            return random.choice(responses)
    return random.choice(QA_PAIRS["default"])

def main():
    print("🤖 AI Chatbot Ready!")
    print("Questions supported:")
    for q in QA_PAIRS.keys():
        print(f"  - {q}")

if __name__ == "__main__":
    main()
