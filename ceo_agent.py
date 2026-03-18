#!/usr/bin/env python3
"""
CEO Agent - Makes high-level decisions
Runs every 30 minutes
"""
import os
import json
from datetime import datetime

REPORT_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/ceo_report.md"

def ceo_review():
    """CEO reviews company status and makes decisions"""
    
    # Check company metrics
    orders_file = "/Users/macbookpro/.openclaw/workspace/company/automation/data/orders.json"
    jobs_file = "/Users/macbookpro/.openclaw/workspace/company/automation/data/jobs.json"
    
    orders = 0
    jobs = 0
    
    if os.path.exists(orders_file):
        with open(orders_file) as f:
            orders = len(json.load(f))
    
    if os.path.exists(jobs_file):
        with open(jobs_file) as f:
            jobs = len(json.load(f))
    
    # Make decisions based on status
    decisions = []
    
    if orders == 0:
        decisions.append("⚠️ No orders yet - increase marketing push")
    
    if jobs == 0:
        decisions.append("📋 No job leads - need to scout more")
    
    if orders > 0:
        decisions.append("💰 Revenue coming in!")
    
    report = f"""# CEO Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📊 Company Metrics

| Metric | Value |
|--------|-------|
| Orders | {orders} |
| Job Leads | {jobs} |
| Website | ✅ Up |

## 🎯 CEO Decisions

{chr(10).join(['- ' + d for d in decisions]) if decisions else '- Keep running normally'}

## 📋 Action Items for PM

1. Scout new jobs
2. Check for orders
3. Run marketing

---
*CEO: EveryCompanyClaw*
"""
    
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    
    print(f"👔 CEO: Reviewed company - Orders: {orders}, Jobs: {jobs}")
    return report

if __name__ == "__main__":
    ceo_review()
