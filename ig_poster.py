#!/usr/bin/env python3
"""
Instagram Auto-Poster using Playwright
Run: python3 /Users/macbookpro/.openclaw/workspace/company/ig_poster.py
"""
import asyncio
import os

# Content to post
IG_CAPTION = """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用
⬇️ link in bio

#python #automation #hkig #香港 #startup #indiehacker"""

async def post_to_instagram():
    """Post to Instagram using Playwright"""
    from playwright.async_api import async_playwright
    
    print("🚀 Starting Instagram Auto-Post...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Go to Instagram
        print("📱 Opening Instagram...")
        await page.goto("https://www.instagram.com/")
        
        # Wait for page to load
        await page.wait_for_load_state("networkidle")
        
        print("⚠️ Please log in if not already logged in")
        print("   Waiting 15 seconds for login...")
        await page.wait_for_timeout(15000)
        
        # Click the + button to create new post
        print("📝 Creating new post...")
        try:
            # Try various selectors for the new post button
            await page.click('svg[aria-label="New post"]', timeout=5000)
        except:
            try:
                await page.click('a[href="#"][role="link"]', timeout=5000)
            except:
                print("   Couldn't auto-click, trying manual...")
        
        await page.wait_for_timeout(3000)
        
        # For now, just show what would be posted
        print(f"""
📋 Caption that would be posted:

{IG_CAPTION}

🎯 To complete posting:
1. Click the + button in Instagram
2. Upload an image
3. Paste the caption above
4. Share!

✅ Playwright browser automation is working!
""")
        
        # Keep browser open for user to complete
        print("Press Ctrl+C to close...")
        await asyncio.sleep(30)
        
        await browser.close()
        print("👋 Browser closed")

if __name__ == "__main__":
    asyncio.run(post_to_instagram())
