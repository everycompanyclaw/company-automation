#!/usr/bin/env python3
"""
Company Auto-Run - With Auto-Install
Ensures all tools are installed before running
"""
import subprocess
import sys
import os

COMPANY_PATH = "/Users/macbookpro/.openclaw/workspace/company"

# Tools that need to be installed
REQUIRED_PACKAGES = [
    "requests",
    "stripe", 
    "playwright"
]

def install_tools():
    """Auto-install required packages"""
    print("🔧 Checking tools...")
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
            print(f"  ✅ {pkg}")
        except ImportError:
            print(f"  ⬇️ Installing {pkg}...")
            subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-q"])
    print("🔧 Tools ready!")

def run_aggressive_learn():
    """Run profit learning"""
    print("🧠 Running profit learning...")
    try:
        result = subprocess.run(
            [sys.executable, f"{COMPANY_PATH}/aggressive_learn.py"],
            capture_output=True, timeout=60
        )
        print(result.stdout.decode() if result.stdout else "Done")
    except Exception as e:
        print(f"Error: {e}")

def run_operations():
    """Run company operations"""
    print("⚙️ Running operations...")
    try:
        subprocess.run([sys.executable, f"{COMPANY_PATH}/auto_run.py"], 
                      capture_output=True, timeout=60)
    except:
        pass

def main():
    print("=" * 50)
    print("🏢 EveryCompanyClaw - AUTO-RUN")
    print("=" * 50)
    
    # Always install tools first
    install_tools()
    
    # Run learning
    run_aggressive_learn()
    
    # Run operations
    run_operations()
    
    print("=" * 50)
    print("✅ Cycle complete")
    print("=" * 50)

if __name__ == "__main__":
    os.chdir(COMPANY_PATH)
    main()
