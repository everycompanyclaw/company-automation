#!/usr/bin/env python3
"""
Email Sequences - Marketing sequences
"""
from datetime import datetime

SEQUENCES = {
    "welcome": {
        "subject": "Welcome! Here's what we do",
        "body": """Hi there!

Thanks for reaching out to EveryCompany!

We help businesses with:
- AI Automation
- Marketing Automation  
- Business Efficiency

Here's a quick guide to get started:
[Link to services]

Looking forward to helping you!

Best,
EveryCompany Team"""
    },
    
    "followup": {
        "subject": "Just checking in",
        "body": """Hi!

Just wanted to follow up on our last message.

Have you had a chance to think about automation for your business?

Here are some quick wins:
- Save 10+ hours/week with AI
- Automate repetitive tasks
- Focus on what matters

DM me if you'd like to chat!

Best,
EveryCompany"""
    },
    
    "value": {
        "subject": "Here's something valuable",
        "body": """Hi!

Here's a free resource for you:

🎯 "5 AI Tools That Actually Work for Small Business"

Download: [link]

These tools helped our clients save time and money!

Let me know if you'd like more tips!

Best,
EveryCompany"""
    },
    
    "close": {
        "subject": "Last chance - let's chat",
        "body": """Hi!

This is my last email (for now)!

If you're interested in:
- Automating your business
- Saving time
- Growing faster

Let's schedule a quick chat - no pressure!

Reply "YES" to book a time.

Best,
EveryCompany"""
    }
}

def generate_sequence():
    """Generate email sequence"""
    return f"""📧 Email Sequence Created

Sequence: 4 emails
1. Welcome - Introduction
2. Follow-up - After 2 days  
3. Value - After 5 days (with free resource)
4. Close - After 7 days (CTA)

Total: 4 emails over 7 days
"""

def main():
    print(generate_sequence())
    print("\nSequences:")
    for key, seq in SEQUENCES.items():
        print(f"\n{key.upper()}:")
        print(f"  Subject: {seq['subject']}")
        print(f"  Body preview: {seq['body'][:50]}...")

if __name__ == "__main__":
    main()