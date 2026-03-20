#!/usr/bin/env python3
"""
Instagram Auto-Poster - Force click Share
"""
from playwright.sync_api import sync_playwright
import time

IG_CAPTION = """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

💰 $79 = 永久使用

#python #automation #hkig #香港"""

def main():
    print("🚀 Opening Instagram...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://www.instagram.com/")
        time.sleep(5)
        
        print("""
1. Click + → Upload → Click Next
2. Wait for caption box
""")
        
        time.sleep(25)
        
        # Fill caption
        page.keyboard.press("Tab")
        time.sleep(0.2)
        page.keyboard.press("Tab")
        time.sleep(0.2)
        page.keyboard.type(IG_CAPTION, delay=3)
        
        time.sleep(2)
        
        # Force click via JS - multiple attempts
        print("🔄 Clicking Share...")
        
        for i in range(10):
            page.evaluate('''
                () => {
                    // Try all buttons
                    document.querySelectorAll('button').forEach(b => {
                        if(b.textContent.includes('Share') || b.textContent.includes('分享')) {
                            b.click();
                            b.dispatchEvent('click');
                            b.dispatchEvent('mousedown');
                        }
                    });
                }
            ''')
            page.keyboard.press("Enter")
            time.sleep(0.5)
        
        print("✅ Done! Check if posted!")
        browser.close()

if __name__ == "__main__":
    main()
