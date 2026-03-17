#!/usr/bin/env python3
"""
24/7 Company Runner
"""
import os
import time
import requests
import subprocess

COMPANY_BOT = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"

def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{COMPANY_BOT}/sendMessage",
                      json={"chat_id": "96691420", "text": text}, timeout=10)
    except:
        pass

def run_jobs():
    try:
        result = subprocess.run(
            ["python3", "/Users/macbookpro/.openclaw/workspace/income-automation/jobs.py"],
            capture_output=True, timeout=60
        )
        if "new jobs" in result.stdout.decode().lower():
            return "New jobs found!"
    except:
        pass
    return None

def run_crypto():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd", timeout=10)
        data = r.json()
        return f"Crypto: BTC ${data['bitcoin']['usd']:,} ETH ${data['ethereum']['usd']}"
    except:
        return None

def main():
    while True:
        # Check jobs every 4 hours
        jobs = run_jobs()
        if jobs:
            send_msg(f"🏢 {jobs}")
        
        # Check crypto every hour
        crypto = run_crypto()
        if crypto:
            print(crypto)
        
        time.sleep(3600)  # 1 hour

if __name__ == "__main__":
    main()
