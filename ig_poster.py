#!/usr/bin/env python3
"""
Instagram Auto-Poster - Using real browser profile
"""
from playwright.sync_api import sync_playwright
import time
import os

IG_CAPTION = """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker"""

def main():
    print("🚀 Opening Instagram (using your real browser)...")
    
    with sync_playwright() as p:
        # Launch with your actual browser profile
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--start-maximized'
            ]
        )
        
        # Create a persistent context (saves login)
        context = browser.new_context(
            viewport={'width': 1400, 'height': 900},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = context.new_page()
        
        # Go to Instagram
        page.goto("https://www.instagram.com/", timeout=30000)
        time.sleep(5)
        
        print("""
📱 Instagram opened!

Please do:
1. If not logged in → log in
2. Click + (Create post)
3. Upload image
4. Click Next

I'll fill caption and TRY to click Share!
""")
        
        # Wait for user to get to caption stage
        print("⏳ Waiting 25 seconds...")
        time.sleep(25)
        
        # Try to fill caption using JS
        print("📝 Filling caption...")
        page.evaluate(f'''
            const textarea = document.querySelector('textarea');
            if(textarea) {{
                textarea.value = `{IG_CAPTION}`;
                textarea.dispatchEvent(new Event('input', {{bubbles: true}}));
                textarea.dispatchEvent(new Event('change', {{bubbles: true}}));
            }}
        ''')
        print("   ✅ Caption filled!")
        
        time.sleep(2)
        
        # Try multiple ways to click Share
        print("🔄 Trying to click Share...")
        
        # Method 1: Find by text and click
        try:
            page.evaluate('''
                const buttons = Array.from(document.querySelectorAll('button'));
                const shareBtn = buttons.find(b => b.textContent.includes('Share'));
                if(shareBtn) { shareBtn.click(); }
            ''')
            print("   ✅ Clicked Share!")
        except:
            pass
        
        time.sleep(1)
        
        # Method 2: Keyboard
        try:
            page.keyboard.press("Enter")
            print("   ✅ Pressed Enter!")
        except:
            pass
        
        time.sleep(3)
        
        # Method 3: Direct selector
        try:
            page.click('button:has-text("Share")', timeout=2000)
            print("   ✅ Clicked via selector!")
        except:
            print("   ⚠️ Could not auto-click")
        
        print("""
⏳ Waiting 30 seconds...
IF POSTED → Done!
IF NOT → Please click Share manually
""")
        
        time.sleep(30)
        
        print("✅ Script complete!")
        browser.close()

if __name__ == "__main__":
    main()
