#!/usr/bin/env python3
"""
Disable NotifyBot messages - Redirect to CompanyBot
"""
# This script shows which files send to NotifyBot
# To disable, update those files to use CompanyBot instead

NOTIFY_BOT = "8677779317:AAEaxRQmEpymFeer0sVPXe1YNMUqcURZACg"
COMPANY_BOT = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"

print("To redirect NotifyBot to CompanyBot:")
print("1. Find all files with NotifyBot token")
print("2. Replace with CompanyBot token")
print(f"\nNotifyBot: {NOTIFY_BOT}")
print(f"CompanyBot: {COMPANY_BOT}")

# Files to check:
files = [
    "weekly_report.py",
    "auto_report.py", 
    "daily_runner.py",
    "crm_telegram.py"
]

print("\nFiles to update:")
for f in files:
    print(f"  - {f}")
