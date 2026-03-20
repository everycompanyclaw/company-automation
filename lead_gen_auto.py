#!/usr/bin/env python3
"""
Lead Generation Automation - Find and engage potential clients
"""
import os
import json
import random
from datetime import datetime

COMPANY_PATH = "/Users/macbookpro/.openclaw/workspace/company"
TELEGRAM_BOT = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"

# Industries to target
INDUSTRIES = [
    "中小企", "餐廳", "診所", "網店", "物流",
    "零售", "教育中心", "美容院", "健身室", "cafe"
]

# Pain points
PAIN_POINTS = [
    "人工高", "無時間處理admin", "想自動化",
    "想慳錢", "想增加效率", "唔識用科技"
]

# Solution templates
SOLUTIONS = [
    "AI自動化可以幫你慳50%時間",
    "我既方案可以幫你減少80%既admin時間",
    "用AI工具可以每月慳幾千蚊",
    "自動化流程可以讓你專注係核心業務"
]

def generate_lead_message():
    """Generate personalized outreach message"""
    industry = random.choice(INDUSTRIES)
    pain = random.choice(PAIN_POINTS)
    solution = random.choice(SOLUTIONS)
    
    templates = [
        f"Hi，我睇到你係{industry}既老板姐，你想解決{pain}既問題嗎？{solution}DM我傾下!",
        
        f"你好，我係EveryCompany既AI助手。如果你既{industry}業務遇到{pain}，我可以幫到你!{solution}",
        
        f"搵咗你好耐! 我地專幫{industry}解決{pain}既困擾。{solution}可以約時間傾下?"
    ]
    
    return random.choice(templates)

def main():
    print("🎯 Lead Generation Auto")
    msg = generate_lead_message()
    print(f"Generated: {msg}")
    
    # Save to leads
    with open(f"{COMPANY_PATH}/automation/data/leads.md", "a") as f:
        f.write(f"\n## {datetime.now().strftime('%Y-%m-%d')}\n{msg}\n")

if __name__ == "__main__":
    main()
