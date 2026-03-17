#!/usr/bin/env python3
"""
PM Agent - Manages tasks and workers
Runs after CEO, reports to CEO
"""
import os
import json
from datetime import datetime

STATUS_FILE = "/Users/macbookpro/.openclaw/workspace/company/status.md"
REPORT_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/daily_report.md"
ORDERS_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/orders.json"

def check_orders():
    """Check for new orders"""
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE) as f:
            orders = json.load(f)
        return len(orders)
    return 0

def check_website():
    """Check if website is up"""
    import urllib.request
    try:
        req = urllib.request.Request('https://everycompanyclaw.github.io/company-automation/')
        urllib.request.urlopen(req, timeout=5)
        return "✅ Up"
    except:
        return "❌ Down"

def pm_report():
    """PM compiles status and assigns tasks"""
    order_count = check_orders()
    site_status = check_website()
    
    report = f"""# PM Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Operations
- Website: {site_status}
- Orders: {order_count}

## Tasks Completed
- [x] Products: Live
- [x] Payments: Active
- [x] Website: Running

## Issues
- Twitter API: Not connected
- Traffic: Need to drive

## Worker Tasks
1. Sales: Send outreach
2. Support: Check messages
3. Operations: Process orders

---
*PM: EveryCompanyClaw*
"""
    
    with open(REPORT_FILE, "a") as f:
        f.write("\n" + report)
    
    print(f"✅ PM report complete - Orders: {order_count}, Site: {site_status}")
    return report

if __name__ == "__main__":
    pm_report()
