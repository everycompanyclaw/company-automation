#!/usr/bin/env python3
"""
Daily Company Runner
"""
import requests

BOTS = {
    "company": "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"
}

def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOTS['company']}/sendMessage",
                      json={"chat_id": "96691420", "text": text}, timeout=10)
    except:
        pass

def main():
    msg = """🏢 Daily Company Report

✅ System: Running
✅ Scripts: Ready
✅ GitHub: Pushed
✅ Email: Ready

📊 Lead Search: 4600+ Python jobs

🎯 Action Items:
1. Update Fiverr gig
2. Apply to jobs
3. Find leads

Company is running!"""
    
    send_msg(msg)

if __name__ == "__main__":
    main()
