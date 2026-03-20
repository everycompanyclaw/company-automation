#!/usr/bin/env python3
"""
Instagram Business Account Switcher
"""
from playwright.sync_api import sync_playwright
import time

def main():
    print("🚀 Opening Instagram Settings...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Go to settings
        page.goto("https://www.instagram.com/accounts/manage_accessibility/")
        time.sleep(5)
        
        # Try settings
        page.goto("https://www.instagram.com/settings/accounts/")
        time.sleep(5)
        
        print("""
📱 Instagram Settings Opened!

Please:
1. Look for "Switch to Professional Account"
2. Click it
3. Select "Business"
4. Follow prompts

I'll wait 60 seconds...
""")
        
        time.sleep(60)
        
        print("✅ Done!")
        browser.close()

if __name__ == "__main__":
    main()
