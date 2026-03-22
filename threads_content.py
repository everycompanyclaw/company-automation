#!/usr/bin/env python3
"""
Threads Content via Telegram - Send ready content to forward
"""
import random

POSTS = [
    "🚀 AI is changing how we work! \n\n#AI #Automation #Tech #HK #Startup #Business",
    "💡 Did you know? AI can save you 10+ hours per week! \n\n#Productivity #AI #Tips #HKBusiness",
    "🎯 Focus on what you do best, let AI handle the rest. \n\n#Entrepreneur #Startup #AI #Automation",
    "⚡ Quick tip: Start small with automation! \n\n#GrowthHacking #Tips #AI #Business #HK",
    "💰 Want to save money? Automate your business! \n\n#SmallBiz #HK #Automation #Entrepreneur"
]

def get_post():
    return random.choice(POSTS)

def main():
    post = get_post()
    print(post)
    return post

if __name__ == "__main__":
    main()