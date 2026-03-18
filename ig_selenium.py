#!/usr/bin/env python3
"""
Instagram Auto-Poster - Using Selenium with undetected-chromedriver
This is designed to bypass bot detection
"""
import time
import sys

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("Installing undetected-chromedriver...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "selenium", "undetected-chromedriver", "-q"])
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

IG_CAPTION = """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker"""

def main():
    print("🚀 Starting Instagram with undetected-chromedriver...")
    
    # Use undetected_chromedriver
    options = uc.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = uc.Chrome(options=options, version_main=None)
    
    print("📱 Opening Instagram...")
    driver.get("https://www.instagram.com/")
    time.sleep(5)
    
    print("""
📋 Steps:
1. If not logged in → log in manually
2. Click + to create post
3. Upload image
4. Click Next

I'll fill caption and TRY to click Share!
""")
    
    # Wait for user to get to caption screen
    time.sleep(30)
    
    # Try to find and fill caption
    print("📝 Trying to fill caption...")
    try:
        # Find textarea
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        for ta in textareas:
            if ta.is_displayed():
                ta.send_keys(IG_CAPTION)
                print("   ✅ Caption filled!")
                break
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
    
    time.sleep(2)
    
    # Try to click Share
    print("🔄 Trying to click Share...")
    try:
        # Find buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            text = btn.text.lower()
            if "share" in text or "分享" in text:
                if btn.is_displayed() and btn.is_enabled():
                    btn.click()
                    print("   ✅ Clicked Share!")
                    break
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
    
    print("""
⏳ Waiting 30 seconds...
If posted → Done!
If not → Please click Share manually
""")
    
    time.sleep(30)
    
    print("✅ Done!")
    driver.quit()

if __name__ == "__main__":
    main()
