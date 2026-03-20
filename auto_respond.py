#!/usr/bin/env python3
"""
Auto-Respond to Leads - Send personalized responses
"""
import random
from datetime import datetime

RESPONSES = {
    "interested": [
        "Thanks for your interest! I'd love to learn more about your needs. When would be a good time to chat?",
        "Great to hear from you! Can you tell me more about what you're looking for?"
    ],
    "question": [
        "Good question! Let me explain...",
        "Thanks for asking! Here's what you need to know..."
    ],
    "price": [
        "Our services start from $500 HKD. It depends on your specific needs. Would you like a free consultation?",
        "Every project is unique! Let's discuss your requirements. DM me to schedule a call!"
    ],
    "default": [
        "Thanks for reaching out! I'll get back to you within 24 hours.",
        "Thanks for your message! Looking forward to helping you with automation."
    ]
}

def get_response(lead_type="default"):
    """Get personalized response"""
    responses = RESPONSES.get(lead_type, RESPONSES["default"])
    return random.choice(responses)

def main():
    print("📞 Auto-Respond to Leads")
    print("Response templates ready!")
    for key in RESPONSES:
        print(f"  - {key}")

if __name__ == "__main__":
    main()
