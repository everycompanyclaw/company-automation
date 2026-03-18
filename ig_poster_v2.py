#!/usr/bin/env python3
"""
Ultimate Instagram Auto-Poster - Uses your logged-in browser session
"""
from playwright.sync_api import sync_playwright
import time
import json

IG_CAPTION = """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker"""

def find_and_click_share(page):
    """Find and click Share button using multiple methods"""
    
    # Method 1: Query all buttons and find by text
    result = page.evaluate('''
        () => {
            const buttons = document.querySelectorAll('button');
            for(let btn of buttons) {
                const text = btn.textContent.trim().toLowerCase();
                if(text === 'share' || text === '分享' || text.includes('share')) {
                    btn.click();
                    return 'clicked';
                }
            }
            // Try divs with role button
            const divs = document.querySelectorAll('[role="button"]');
            for(let div of divs) {
                const text = div.textContent.trim().toLowerCase();
                if(text === 'share' || text.includes('share')) {
                    div.click();
                    return 'clicked-div';
                }
            }
            return 'not-found';
        }
    ''')
    return result

def main():
    print("🚀 Opening Instagram (persistent session)...")
    
    with sync_playwright() as p:
        # Launch with persistent context (saves login)
        context = p.chromium.launch_persistent_context(
            user_data_dir="/tmp/instagram_persistent",
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage'
            ]
        )
        
        # Check if already logged in
        page = context.new_page()
        
        print("📱 Checking login status...")
        page.goto("https://www.instagram.com/", timeout=30000)
        time.sleep(3)
        
        # Check if logged in
        login_check = page.evaluate('''
            () => {
                const loginBtn = document.querySelector('button[type="submit"]');
                return loginBtn ? 'not-logged-in' : 'logged-in';
            }
        ''')
        
        if login_check == 'not-logged-in':
            print("⚠️ Not logged in! Please log in manually.")
            print("   I'll wait 60 seconds...")
            time.sleep(60)
        
        print("""
📋 Steps:
1. Click + to create post
2. Upload image
3. Click Next
4. I'll auto-fill caption AND click Share!
""")
        
        # Wait for user to get to caption screen
        wait_time = 35
        print(f"⏳ Waiting {wait_time} seconds...")
        time.sleep(wait_time)
        
        # Fill caption
        print("📝 Filling caption...")
        page.evaluate(f'''
            () => {{
                const textareas = document.querySelectorAll('textarea');
                for(let ta of textareas) {{
                    ta.value = `{IG_CAPTION}`;
                    ta.dispatchEvent(new Event('input', {{bubbles: true}}));
                    ta.dispatchEvent(new Event('change', {{bubbles: true}}));
                }}
            }}
        ''')
        print("   ✅ Caption filled!")
        
        time.sleep(2)
        
        # Try to click Share - multiple attempts
        print("🔄 Attempting to click Share (will try 3 times)...")
        
        for attempt in range(3):
            result = find_and_click_share(page)
            print(f"   Attempt {attempt+1}: {result}")
            
            if result == 'clicked' or result == 'clicked-div':
                print("   ✅ CLICKED!")
                break
            
            time.sleep(2)
        
        # Final wait
        print("⏳ Final wait - if posted, great! If not, I'll close...")
        time.sleep(15)
        
        print("✅ Done! Check if posted!")
        context.close()

if __name__ == "__main__":
    main()
