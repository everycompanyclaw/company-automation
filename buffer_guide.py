#!/usr/bin/env python3
"""
Buffer API - Guide user through creation
"""
from playwright.sync_api import sync_playwright
import time

def guide_buffer():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Go to developers
        page.goto("https://buffer.com/developers")
        time.sleep(3)
        
        print("""
📋 BUFFER API SETUP
=================

On the page:

1. Click 'My Apps' (top right)
2. Click 'Create an App'

Form details:
- App Name: EveryCompanyClaw
- Homepage URL: https://everycompanyclaw.github.io/company-automation/
- Description: AI company that automates posts
- Redirect URI: http://localhost

3. Click 'Create App'

4. On next page, find 'Access Tokens'
5. Copy the token

I'll wait 2 minutes for you to do this!
""")
        
        time.sleep(120)
        
        print("Done? Copy the token and give it to me!")
        browser.close()

guide_buffer()
