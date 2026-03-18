#!/usr/bin/env python3
"""
CEO - PROFIT FOCUSED
No job hunting - only money-making decisions
"""
import os
import json
from datetime import datetime

def ceo_decisions():
    """Only profit-focused decisions"""
    
    # Check revenue
    orders_file = "/Users/macbookpro/.openclaw/workspace/company/automation/data/orders.json"
    revenue = 0
    
    if os.path.exists(orders_file):
        with open(orders_file) as f:
            orders = json.load(f)
            revenue = sum(o.get('amount', 0) for o in orders) / 100
    
    # Profit-focused decisions
    decisions = []
    
    if revenue == 0:
        decisions = [
            "🚨 REVENUE $0 - EMERGENCY",
            "1. Post to Instagram NOW",
            "2. Send more marketing",
            "3. Offer discount for first customer"
        ]
    else:
        decisions = [
            f"💰 Revenue: ${revenue}",
            "1. Continue marketing",
            "2. Create upsell",
            "3. Scale what works"
        ]
    
    report = f"""# CEO Profit Decisions - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 💰 Revenue: ${revenue}

## 🎯 Actions (NO JOB HUNTING)

{chr(10).join([f"{i+1}. {d}" for i, d in enumerate(decisions)])}

## ✅ Focus Areas
- Marketing (Instagram/Telegram)
- Product creation
- Sales optimization
- Customer delight

---
*CEO: EveryCompanyClaw* (Profit Focused)
"""
    
    with open("/Users/macbookpro/.openclaw/workspace/company/automation/data/ceo_decisions.md", "w") as f:
        f.write(report)
    
    print(f"👔 CEO: Revenue ${revenue} - Profit focus!")

if __name__ == "__main__":
    ceo_decisions()
