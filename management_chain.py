#!/usr/bin/env python3
"""
Management Chain - PROFIT FOCUSED
CEO → PM → Workers
Runs every 30 minutes
"""
import subprocess
import sys

def run_ceo():
    """CEO makes profit decisions"""
    print("👔 CEO: Making profit decisions...")
    subprocess.run([sys.executable, "/Users/macbookpro/.openclaw/workspace/company/ceo_agent.py"])

def run_profit():
    """Generate profit"""
    print("💰 Running profit generator...")
    subprocess.run([sys.executable, "/Users/macbookpro/.openclaw/workspace/company/profit_generator.py"])

def run_workers():
    """Workers execute profit actions"""
    print("👷 Workers: Executing tasks...")
    
    # Run job scout
    subprocess.run([sys.executable, "/Users/macbookpro/.openclaw/workspace/company/job_scout.py"])
    
    # Check orders
    subprocess.run([sys.executable, "-c", "import stripe; print('Stripe ready')"], capture_output=True)

def daily_profit_cycle():
    """Full profit cycle"""
    print("=" * 50)
    print("🏢 Company Profit Cycle")
    print("=" * 50)
    
    run_ceo()
    run_profit()
    run_workers()
    
    print("=" * 50)
    print("✅ Profit cycle complete")
    print("=" * 50)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    
    if mode == "ceo":
        run_ceo()
    elif mode == "profit":
        run_profit()
    elif mode == "workers":
        run_workers()
    else:
        daily_profit_cycle()
