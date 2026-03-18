#!/usr/bin/env python3
"""
Instagram Auto-Poster - Uses keyboard only
"""
from playwright.sync_api import sync_playwright
import time
import subprocess

IG_CAPTION = """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker"""

def main():
    print("🚀 Opening Instagram...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        page = browser.new_page()
        page.goto("https://www.instagram.com/")
        time.sleep(5)
        
        print("""
📱 Steps:
1. Click + → Upload image → Click Next
2. I'll fill caption
3. Use AppleScript to click Share!
""")
        
        time.sleep(25)
        
        # Fill caption with JavaScript
        page.evaluate(f'document.execCommand("paste")')
        
        # Try using AppleScript to click
        print("🔄 Using AppleScript to click Share...")
        
        try:
            # Click at coordinates where Share button usually is
            subprocess.run([
                'osascript', '-e', '''
                tell application "System Events"
                    tell process "Chrome"
                        -- Try to find and click Share
                        keystroke return
                    end tell
                end tell
                '''
            ], timeout=5)
            print("   ✅ Tried Enter key")
        except:
            pass
        
        time.sleep(20)
        
        print("✅ Done! Check if posted!")
        browser.close()

if __name__ == "__main__":
    main()
