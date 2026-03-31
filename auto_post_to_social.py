#!/usr/bin/env python3
"""
Instagram & Threads Auto-Poster
Uses Playwright for browser automation to post content

Usage:
    python auto_poster.py --platform instagram --content "Your post caption"
    python auto_poster.py --platform threads --content "Your post caption"  
    python auto_poster.py --platform both --content "Your post caption"

Prerequisites:
    1. Run: npx playwright install chromium
    2. Log in to Instagram/Threads manually in the browser first
    3. The script will use existing browser session
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Try to import playwright, install if needed
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Installing playwright...")
    os.system("pip install playwright")
    from playwright.async_api import async_playwright

CONTENT_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/instagram_threads_content.md"

POSTS = {
    "instagram": [
        """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用
⬇️ link in bio

#python #automation #hkig #香港 #startup #indiehacker #coding #programmer #tech #工具""",
        
        """🤖 我build咗一個AI公司

佢24/7自動運作
自動賣產品、處理訂單、發貨

我就可以做其他嘢

$79起｜everycompanyclaw.github.io

#buildinpublic #automation #ai #entrepreneur"""
    ],
    "threads": [
        """🧵 我build咗一個自己運作既公司

佢會：
- 24/7賣嘢
- 自動收錢 (Stripe)
- 自動發貨

products:
- Python腳本套裝 $79
- Zapier範本 $49  
- AI提示詞 $29

link: everycompanyclaw.github.io/company-automation/

#buildinpublic #startup #hk""",

        """日頭寫code
夜晚瞓覺
一樣有收入

呢個就係自動化既威力

👉 everycompanyclaw.github.io/company-automation/

#automation #passiveincome #sideproject"""
    ]
}

async def post_to_instagram(browser, caption: str, image_path: str = None):
    """Post to Instagram using Playwright"""
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        print("📱 Opening Instagram...")
        await page.goto("https://www.instagram.com/", timeout=30000)
        
        # Wait for either logged-in state or login form
        await page.wait_for_load_state("networkidle")
        
        # Check if logged in (look for home feed)
        try:
            await page.wait_for_selector('main[role="main"]', timeout=5000)
            print("✅ Already logged in to Instagram")
        except:
            print("⚠️ Not logged in. Please log in manually and run again.")
            print("   The browser will stay open for you to log in, then close it manually.")
            await asyncio.sleep(30)
            return False
        
        # Click create new post button
        print("📝 Creating new post...")
        
        # Try various selectors for the create post button
        create_selectors = [
            'svg[aria-label="New post"]',
            'a[href="/creator/"]',
            'svg[aria-label="Create new post"]',
            'button:has-text("Create")'
        ]
        
        for selector in create_selectors:
            try:
                await page.click(selector, timeout=3000)
                print(f"✅ Clicked create button: {selector}")
                break
            except:
                continue
        
        await asyncio.sleep(2)
        
        # If image provided, upload it
        if image_path and os.path.exists(image_path):
            print(f"📤 Uploading image: {image_path}")
            # File input selector
            await page.set_input_files('input[type="file"]', image_path)
            await asyncio.sleep(3)
        
        # Fill in caption
        print("✍️ Adding caption...")
        caption_selectors = [
            'textarea[aria-label="Write a caption..."]',
            'div[contenteditable="true"][role="textbox"]',
            'textarea[placeholder="Write a caption…"]'
        ]
        
        for selector in caption_selectors:
            try:
                await page.fill(selector, caption)
                print(f"✅ Filled caption: {selector}")
                break
            except:
                continue
        
        # Click share/post button
        print("🚀 Sharing post...")
        share_selectors = [
            'button:has-text("Share")',
            'button:has-text("Post")',
            'div[role="button"]:has-text("Share")',
            'button[type="submit"]'
        ]
        
        for selector in share_selectors:
            try:
                await page.click(selector, timeout=3000)
                print(f"✅ Clicked share: {selector}")
                break
            except:
                continue
        
        await asyncio.sleep(3)
        print("✅ Instagram post published!")
        return True
        
    except Exception as e:
        print(f"❌ Error posting to Instagram: {e}")
        return False
    finally:
        await context.close()


async def post_to_threads(browser, caption: str):
    """Post to Threads using Playwright"""
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        print("📘 Opening Threads...")
        await page.goto("https://www.threads.net/", timeout=30000)
        await page.wait_for_load_state("networkidle")
        
        # Check if logged in
        try:
            await page.wait_for_selector('main[role="main"]', timeout=5000)
            print("✅ Logged in to Threads")
        except:
            print("⚠️ Not logged in. Please log in manually.")
            await asyncio.sleep(30)
            return False
        
        # Look for create post button
        print("📝 Creating new thread...")
        
        # Try to find and click the create button
        create_selectors = [
            'svg[aria-label="New thread"]',
            'a[href="/compose/thread"]',
            'button:has-text("Create")',
            'div[role="button"]:has-text("New thread")'
        ]
        
        for selector in create_selectors:
            try:
                await page.click(selector, timeout=3000)
                print(f"✅ Found create button: {selector}")
                break
            except:
                continue
        
        await asyncio.sleep(2)
        
        # Fill in the post
        print("✍️ Writing thread...")
        text_selectors = [
            'div[contenteditable="true"][role="textbox"]',
            'textarea[placeholder="What do you want to say?"]',
            'div[aria-label="Thread text box"]'
        ]
        
        for selector in text_selectors:
            try:
                await page.fill(selector, caption)
                print(f"✅ Filled text: {selector}")
                break
            except:
                continue
        
        # Post
        print("🚀 Posting...")
        post_selectors = [
            'button:has-text("Post")',
            'div[role="button"]:has-text("Post")',
            'button[type="submit"]'
        ]
        
        for selector in post_selectors:
            try:
                await page.click(selector, timeout=3000)
                print(f"✅ Clicked post: {selector}")
                break
            except:
                continue
        
        await asyncio.sleep(3)
        print("✅ Threads post published!")
        return True
        
    except Exception as e:
        print(f"❌ Error posting to Threads: {e}")
        return False
    finally:
        await context.close()


# Top-level argument parser
_parser = argparse.ArgumentParser(description="Auto-post to Instagram & Threads")
_parser.add_argument("--platform", choices=["instagram", "threads", "both"], default="both")
_parser.add_argument("--content", "-c", help="Custom caption (overrides default)")
_parser.add_argument("--post-index", "-i", type=int, default=0, help="Which post to use (0, 1, 2...)")
_parser.add_argument("--image", help="Image file path to post")
_parser.add_argument("--keep-open", action="store_true", help="Keep browser open after posting")
_parser.add_argument("--dry-run", action="store_true", help="Show post content without publishing")

async def main():
    args = _parser.parse_args()
    
    print("🚀 Auto-Poster")
    print(f"   Platform: {args.platform}")
    
    if args.dry_run:
        idx_ig = min(args.post_index, len(POSTS["instagram"]) - 1)
        idx_th = min(args.post_index, len(POSTS["threads"]) - 1)
        print("\n📱 [DRY RUN] Instagram caption:")
        print(POSTS["instagram"][idx_ig])
        print("\n📘 [DRY RUN] Threads caption:")
        print(POSTS["threads"][idx_th])
        return
    
    async with async_playwright() as p:
        # Launch browser (reuse existing session if possible)
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        
        if args.platform in ["instagram", "both"]:
            idx = min(args.post_index, len(POSTS["instagram"]) - 1)
            caption = args.content or POSTS["instagram"][idx]
            print(f"\n📱 Posting to Instagram...")
            await post_to_instagram(browser, caption, args.image)
        
        if args.platform in ["threads", "both"]:
            idx = min(args.post_index, len(POSTS["threads"]) - 1)
            caption = args.content or POSTS["threads"][idx]
            print(f"\n📘 Posting to Threads...")
            await post_to_threads(browser, caption)
        
        if args.keep_open:
            print("\n⏳ Browser kept open. Press Ctrl+C to close.")
            await asyncio.sleep(3600)
        else:
            await asyncio.sleep(2)
        
        await browser.close()
    
    print("\n✅ Done!")


if __name__ == "__main__":
    asyncio.run(main())
