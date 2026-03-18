#!/usr/bin/env python3
"""
CEO Agent - Makes PROFIT-FOCUSED decisions
Runs every 30 minutes
"""
import os
import json
from datetime import datetime

def ceo_profit_decisions():
    """CEO makes decisions that generate profit"""
    
    # Check current status
    orders_file = "/Users/macbookpro/.openclaw/workspace/company/automation/data/orders.json"
    revenue = 0
    
    if os.path.exists(orders_file):
        with open(orders_file) as f:
            orders = json.load(f)
            revenue = sum(o.get('amount', 0) for o in orders) / 100
    
    # Generate profit actions
    actions = []
    
    # If no revenue → focus on MARKETING
    if revenue == 0:
        actions = [
            "URGENT: No revenue!",
            "1. Run Instagram poster NOW",
            "2. Send more marketing",
            "3. Post to multiple platforms",
            "4. Consider discounts to get first sale"
        ]
    # If has revenue → focus on SCALING
    else:
        actions = [
            f"💰 Revenue: ${revenue}",
            "1. Continue marketing",
            "2. Optimize for conversions",
            "3. Create upsell products",
            "4. Build repeat customers"
        ]
    
    report = f"""# CEO Profit Decisions - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 💰 Revenue Status

| Metric | Value |
|--------|-------|
| Revenue | ${revenue} |
| Target | $1000/month |

## 🎯 Profit Actions

{chr(10).join([f"{i+1}. {a}" for i, a in enumerate(actions)])}

## 🚀 Immediate Actions

- Run profit_generator.py
- Post to Instagram
- Send marketing
- Check for orders

---
*CEO: EveryCompanyClaw*
"""
    
    with open("/Users/macbookpro/.openclaw/workspace/company/automation/data/ceo_profit.md", "w") as f:
        f.write(report)
    
    print(f"👔 CEO: Revenue ${revenue} - {len(actions)} actions generated")

if __name__ == "__main__":
    ceo_profit_decisions()
