#!/usr/bin/env python3
"""
Management Chain - CEO → PM → Workers
Automated company hierarchy
"""
import os
import sys
from datetime import datetime

# Add company path
sys.path.insert(0, "/Users/macbookpro/.openclaw/workspace/company")

def run_ceo():
    """CEO makes decisions"""
    print("👔 CEO: Reviewing company status...")
    os.system("python3 /Users/macbookpro/.openclaw/workspace/company/ceo_agent.py")
    print("   → CEO decisions recorded\n")

def run_pm():
    """PM manages tasks"""
    print("📋 PM: Compiling status report...")
    os.system("python3 /Users/macbookpro/.openclaw/workspace/company/pm_agent.py")
    print("   → Tasks assigned to workers\n")

def run_workers():
    """Workers execute tasks"""
    print("👷 Workers: Executing tasks...")
    
    roles = ["sales", "support", "operations"]
    for role in roles:
        os.system(f"python3 /Users/macbookpro/.openclaw/workspace/company/worker_agents.py {role}")
    
    print("   → All workers done\n")

def daily_check():
    """Full daily check - CEO → PM → Workers"""
    print("=" * 50)
    print(f"🏢 Company Check - {datetime.now()}")
    print("=" * 50)
    
    print("\n[1/3] CEO Review...")
    run_ceo()
    
    print("[2/3] PM Report...")
    run_pm()
    
    print("[3/3] Workers Execute...")
    run_workers()
    
    print("=" * 50)
    print("✅ Daily check complete")
    print("=" * 50)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    
    if mode == "ceo":
        run_ceo()
    elif mode == "pm":
        run_pm()
    elif mode == "workers":
        run_workers()
    else:
        daily_check()
