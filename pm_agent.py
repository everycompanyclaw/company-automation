#!/usr/bin/env python3
"""
PM Agent - Manages tasks and workers
Runs every 30 minutes
"""
import os
import json
import subprocess
from datetime import datetime

REPORT_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/pm_report.md"

def check_orders():
    """Check for new orders"""
    orders_file = "/Users/macbookpro/.openclaw/workspace/company/automation/data/orders.json"
    if os.path.exists(orders_file):
        with open(orders_file) as f:
            orders = json.load(f)
        return len(orders)
    return 0

def check_website():
    """Check if website is up"""
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
             "https://everycompanyclaw.github.io/company-automation/"],
            capture_output=True, timeout=10
        )
        if result.stdout.decode() == "200":
            return "✅ Up"
    except:
        pass
    return "⚠️ Down"

def run_job_scout():
    """Run job scouting"""
    try:
        subprocess.run(
            ["python3", "/Users/macbookpro/.openclaw/workspace/company/job_scout.py"],
            capture_output=True, timeout=30
        )
        return "✅ Job scout ran"
    except Exception as e:
        return f"⚠️ Job scout failed: {e}"

def pm_report():
    """PM compiles status and assigns tasks"""
    order_count = check_orders()
    site_status = check_website()
    job_result = run_job_scout()
    
    report = f"""# PM Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📊 Operations

| Task | Status |
|------|--------|
| Website | {site_status} |
| Orders | {order_count} |
| Job Scout | {job_result} |

## 👷 Worker Tasks

1. Sales: Check for new leads
2. Support: Monitor messages  
3. Operations: Process orders

## ⚠️ Issues to Escalate

{'- None' if order_count > 0 else '- No orders yet - need more marketing'}

---
*PM: EveryCompanyClaw*
"""
    
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    
    print(f"📋 PM: Report complete - Orders: {order_count}, Site: {site_status}")
    return report

if __name__ == "__main__":
    pm_report()
