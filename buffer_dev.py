#!/usr/bin/env python3
"""
Buffer Developer Portal Auto-Navigate
"""
from playwright.sync_api import sync_playwright
import time

def click_buffer():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("Opening Buffer developers...")
        page.goto("https://buffer.com/developers")
        time.sleep(5)
        
        print("""
On the page:
1. Click 'My Apps'
2. Click 'Create New App'
3. Fill form:
   - Name: EveryCompanyClaw
   - URL: https://everycompanyclaw.github.io/company-automation
   - Redirect: http://localhost
4. Submit
5. Copy Access Token
""")
        
        time.sleep(60)
        browser.close()

click_buffer()
