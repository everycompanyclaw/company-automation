#!/usr/bin/env python3
"""
Threads Auto-Poster — Threads only
Posts to Threads using Playwright browser automation.

Usage:
    python3 threads_poster.py              # Post one random thread
    python3 threads_poster.py --dry-run    # Show what would be posted

Requirements:
    1. Run: playwright install chromium
    2. Log in to threads.net manually in the browser ONCE
       (session cookies will be saved and reused)
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Installing playwright...")
    os.system("pip install playwright")
    from playwright.async_api import async_playwright

POSTS = [
    """🚀 Built a company that runs itself 24/7

While I sleep, it:
- sells products automatically
- handles payments via Stripe
- ships digital goods instantly

Products from $29 → everycompanyclaw.github.io

#buildinpublic #startup #ai #automation #entrepreneur #sideproject""",

    """💡 The best businesses scale without you

I built an AI company that:
- runs around the clock
- costs almost nothing to operate
- sells automatically

Start from $29: everycompanyclaw.github.io

#passiveincome #automation #aibusiness #entrepreneur #startup""",

    """⚡ I automated my entire business

Now I:
- wake up to sales notifications
- don't handle support tickets
- don't manually post on social

The secret? AI agents + good automation.

everycompanyclaw.github.io

#automation #entrepreneur #ai #businesstips #startup""",

    """🎯 Built this in days, not months

Most people overthink starting a business.

I used:
- AI agents to do the work
- Stripe for payments
- GitHub Pages for hosting
- OpenClaw to run it 24/7

$29 starter: everycompanyclaw.github.io

#buildinpublic #startup #ai #tech #indiehacker""",

    """🧵 My AI company made its first sales

Zero marketing budget.
Zero employees.
Just agents running while I sleep.

Products from $29 → everycompanyclaw.github.io

#aicompanies #buildinpublic #startup #ai #entrepreneur""",

    """🌙 The future is AI + human oversight

I don't run my company.
I supervise it.

The agents do:
- customer service
- lead gen
- content creation
- payments

EverycompanyClaw — everycompanyclaw.github.io

#futureofwork #ai #automation #business #startup""",
]


async def post_to_threads(dry_run: bool = False) -> bool:
    """Post to Threads using Playwright. Returns True on success."""

    cookies_path = Path("/tmp/threads_cookies.json")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=500,
            args=["--start-maximized"]
        )

        context = await browser.new_context(
            storage_state=str(cookies_path) if cookies_path.exists() else None
        )
        page = await context.new_page()

        try:
            print("📘 Opening Threads.net...")
            await page.goto("https://www.threads.net/", timeout=30000)
            await page.wait_for_load_state("networkidle")

            # Check if logged in
            try:
                await page.wait_for_selector('a[href="/[username]"]', timeout=5000)
                print("✅ Logged in to Threads")
            except:
                print("⚠️ Not logged in. Opening login page...")
                await page.goto("https://www.threads.net/login", timeout=15000)
                await page.wait_for_load_state("networkidle")
                print("   Please log in manually. Browser will stay open for 60 seconds.")
                await asyncio.sleep(60)
                # Save cookies for next time
                await context.storage_state(path=str(cookies_path))
                print("✅ Session saved. Re-run to post.")
                return False

            # Click create new thread button
            print("📝 Creating new thread...")
            create_selectors = [
                'a[href="/compose/thread"]',
                'svg[aria-label="New thread"]',
                'div[role="button"][tabindex="0"]',
            ]
            clicked = False
            for selector in create_selectors:
                try:
                    await page.click(selector, timeout=3000)
                    print(f"✅ Clicked: {selector}")
                    clicked = True
                    break
                except:
                    continue

            if not clicked:
                # Try navigating directly to compose
                await page.goto("https://www.threads.net/compose/thread", timeout=15000)
                await page.wait_for_load_state("networkidle")

            await asyncio.sleep(2)

            # Fill the post text
            text_selectors = [
                'div[contenteditable="true"][role="textbox"]',
                'div[aria-label="Thread text box"]',
                'textarea[placeholder="What do you want to say?"]',
            ]
            post_text = POSTS[0]  # default
            filled = False
            for selector in text_selectors:
                try:
                    await page.fill(selector, post_text)
                    print(f"✅ Filled text: {selector}")
                    filled = True
                    break
                except:
                    continue

            if not filled:
                print("❌ Could not find text box")
                return False

            if dry_run:
                print(f"✅ [DRY RUN] Would post:\n{post_text}")
                return True

            # Post
            print("🚀 Posting...")
            post_selectors = [
                'button:has-text("Post")',
                'div[role="button"]:has-text("Post")',
                'button[type="submit"]',
            ]
            for selector in post_selectors:
                try:
                    await page.click(selector, timeout=3000)
                    print(f"✅ Clicked post: {selector}")
                    break
                except:
                    continue

            await asyncio.sleep(4)
            print("✅ Threads post published!")
            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        finally:
            await context.close()
            await browser.close()


async def main():
    parser = argparse.ArgumentParser(description="Post to Threads")
    parser.add_argument("--dry-run", action="store_true", help="Show post without publishing")
    args = parser.parse_args()

    print("📘 Threads Auto-Poster")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'LIVE'}\n")

    success = await post_to_threads(dry_run=args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
