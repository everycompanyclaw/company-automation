#!/usr/bin/env python3
"""
Instagram Auto-Poster - Full Auto with JavaScript
"""
from playwright.sync_api import sync_playwright
import time

IG_CAPTION = """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker"""

def click_share_js(page):
    """Try multiple JavaScript methods to click Share"""
    methods = [
        # Method 1: Find and click any Share button
        'document.querySelectorAll("button").forEach(b => { if(b.innerText.includes("Share")) b.click() })',
        
        # Method 2: Find button with role
        'document.querySelectorAll("[role=button]").forEach(b => { if(b.innerText && b.innerText.includes("Share")) b.click() })',
        
        # Method 3: Keyboard Enter
        'document.activeElement.dispatchEvent(new KeyboardEvent("keydown", {key: "Enter", bubbles: true}))',
        
        # Method 4: Form submit
        'document.querySelectorAll("form").forEach(f => f.submit())',
    ]
    
    for i, js in enumerate(methods, 1):
        try:
            result = page.evaluate(js)
            print(f"   Method {i}: Executed")
            time.sleep(1)
        except Exception as e:
            print(f"   Method {i}: {e}")

def main():
    print("🚀 Opening Instagram...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False, 
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        page = browser.new_page()
        
        # Set realistic viewport
        page.set_viewport_size({"width": 1280, "height": 720})
        
        page.goto("https://www.instagram.com/")
        time.sleep(4)
        
        print("""
📱 Instagram opened!

1. Click + → 2. Upload image → 3. Click Next
I'll handle the rest!
""")
        
        # Wait for user to get to caption screen
        time.sleep(20)
        
        # Fill caption using keyboard
        print("📝 Filling caption...")
        page.keyboard.press("Tab")
        time.sleep(0.3)
        page.keyboard.press("Tab")
        time.sleep(0.3)
        page.keyboard.type(IG_CAPTION, delay=3)
        print("✅ Caption filled!")
        
        time.sleep(2)
        
        # Try to click Share
        print("🔄 Attempting to click Share...")
        
        # Method 1: JavaScript click
        click_share_js(page)
        
        # Method 2: Try keyboard Enter
        print("   Trying Enter key...")
        page.keyboard.press("Enter")
        time.sleep(1)
        page.keyboard.press("Enter")
        
        time.sleep(3)
        
        # Method 3: Find button and click
        print("   Trying button search...")
        try:
            page.evaluate('''
                const buttons = Array.from(document.querySelectorAll('button'));
                const shareBtn = buttons.find(b => b.textContent.includes('Share') || b.textContent.includes('分享'));
                if(shareBtn) { shareBtn.click(); console.log('Clicked!'); }
            ''')
        except:
            pass
        
        print("""
⏳ Waiting 20 seconds...
If not posted, please click Share manually
""")
        
        time.sleep(20)
        
        print("✅ Done!")
        browser.close()

if __name__ == "__main__":
    main()
