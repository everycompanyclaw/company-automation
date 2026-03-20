#!/usr/bin/env python3
"""
Instagram Auto-Post - No Asking Version
Run this and it automatically posts
"""
from playwright.sync_api import sync_playwright
import time
import sys

POSTS = [
    """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker""",
    
    """🤖 我build咗一個AI公司

24/7自動運作
自動賣產品、收錢、發貨

$79起｜everycompanyclaw.github.io

#buildinpublic #automation #ai""",
    
    """💰 Python Scripts Bundle - $79

20個自動化腳本：
- Email提取器
- 檔案整理器
- 發票生成器
- CSV/JSON轉換

即時下載：everycompanyclaw.github.io

#automation #python #香港""",
]

def get_caption():
    """Get next caption"""
    idx = int(time.time()) % len(POSTS)
    return POSTS[idx]

def post():
    """Post to Instagram"""
    caption = get_caption()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://www.instagram.com/")
        time.sleep(5)
        
        # Wait for user to create post
        print("Waiting for you to create post (upload image + click Next)...")
        time.sleep(30)
        
        # Fill caption
        page.keyboard.press("Tab")
        time.sleep(0.2)
        page.keyboard.press("Tab")
        time.sleep(0.2)
        page.keyboard.type(caption, delay=3)
        
        print("Caption filled!")
        
        # Try to click Share
        for _ in range(5):
            page.keyboard.press("Enter")
            time.sleep(1)
        
        print("Done! Check if posted!")
        
        time.sleep(15)
        browser.close()

if __name__ == "__main__":
    print("🚀 Auto-posting to Instagram...")
    post()
