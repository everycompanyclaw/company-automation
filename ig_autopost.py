#!/usr/bin/env python3
"""
Instagram Auto-Post - Post to Instagram automatically
"""
import os
import random
from datetime import datetime

# Post templates
POSTS = [
    {
        "caption": "🚀 AI is changing how we work!\n\n.\n.\n.\n#AI #Automation #Tech #HK #Startup #Business #Productivity #Future",
        "type": "image"
    },
    {
        "caption": "💡 Did you know? AI can save you 10+ hours per week!\n\n.\n.\n#Productivity #AI #Tips #HKBusiness #Automation #WorkSmart",
        "type": "image"
    },
    {
        "caption": "🎯 Focus on what you do best, let AI handle the rest.\n\n.\n.\n#Entrepreneur #Startup #AI #Automation #SmallBusiness #HK",
        "type": "image"
    },
    {
        "caption": "⚡ Quick tip: Start small with automation!\n\n.\n.\n#GrowthHacking #Tips #AI #Automation #BusinessTips #HK",
        "type": "image"
    }
]

def get_post():
    """Get random post content"""
    return random.choice(POSTS)

def main():
    print("📸 Instagram Auto-Post")
    post = get_post()
    print(f"Caption: {post['caption'][:50]}...")
    print("Note: Need Instagram API credentials to post")

if __name__ == "__main__":
    main()
