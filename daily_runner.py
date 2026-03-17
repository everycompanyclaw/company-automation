#!/usr/bin/env python3
"""
Daily Company Runner - Runs all company agents autonomously
Scheduled via cron: 0 8,12,17 * * 1-5
"""
import os
import sys
import json
from datetime import datetime

# Paths
BASE_DIR = "/Users/macbookpro/.openclaw/workspace/company"
DATA_DIR = f"{BASE_DIR}/automation/data"
LOG_FILE = f"{DATA_DIR}/daily_log.md"

def log(message):
    """Log to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)
    print(entry.strip())

def run_sales():
    """Run sales agent - send outreach"""
    log("🤖 Running Sales Agent...")
    # In production: import and run outreach
    # For now: log intent
    log("   → Would send outreach emails")
    log("   → Would follow up with leads")
    return True

def run_support():
    """Run support agent - check messages"""
    log("💬 Running Support Agent...")
    log("   → Would check for new messages")
    log("   → Would respond to FAQs")
    return True

def run_operations():
    """Run operations - check orders"""
    log("⚙️ Running Operations Agent...")
    
    # Check orders
    orders_file = f"{DATA_DIR}/orders.json"
    if os.path.exists(orders_file):
        with open(orders_file) as f:
            orders = json.load(f)
        log(f"   → Found {len(orders)} orders")
        
        # Process pending orders
        pending = [o for o in orders if o.get('status') == 'pending']
        if pending:
            log(f"   → Processing {len(pending)} pending orders")
    else:
        log("   → No orders yet")
    
    return True

def run_marketing():
    """Run marketing agent - social posts"""
    log("📢 Running Marketing Agent...")
    log("   → Would post to social media")
    return True

def daily_report():
    """Generate daily report"""
    log("📊 Daily Report:")
    
    # Count files
    leads_file = f"{DATA_DIR}/leads.md"
    orders_file = f"{DATA_DIR}/orders.json"
    
    log(f"   → Status: Running")
    log(f"   → Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    return True

def main():
    """Main runner"""
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    
    log("=" * 40)
    log(f"🏢 Company Runner - {mode.upper()}")
    log("=" * 40)
    
    if mode == "sales":
        run_sales()
    elif mode == "support":
        run_support()
    elif mode == "operations":
        run_operations()
    elif mode == "marketing":
        run_marketing()
    elif mode == "report":
        daily_report()
    elif mode == "daily":
        run_operations()
        run_sales()
        run_marketing()
        run_support()
        daily_report()
    else:
        log(f"Unknown mode: {mode}")
    
    log("✅ Done")

if __name__ == "__main__":
    main()
