#!/usr/bin/env python3
"""
MiniMax-Powered Social Media Content Generator
Uses MiniMax API (web_search + generate) to create trending content.

Usage:
    python3 content_generator.py                  # Generate posts for today
    python3 content_generator.py --topic "AI"   # Search specific topic
    python3 content_generator.py --dry-run      # Show what would be generated

Requirements:
    - MINIMAX_API_KEY env var set
    - Or edit API_KEY below
"""

import os
import sys
import json
import requests
import argparse
from datetime import datetime

# ===== CONFIG =====
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
API_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")
MODEL = "MiniMax-Text-01"  # or MiniMax-Text-01

# Fallback content themes if no API key
FALLBACK_TOPICS = [
    "AI automation business",
    "build in public startup",
    "passive income automation",
    "indie hacker tools",
    "AI company 24/7",
]


def search_web(query: str) -> list:
    """Search the web using MiniMax MCP tool via direct API."""
    if not API_KEY:
        print("⚠️ MINIMAX_API_KEY not set — using fallback topics")
        return []

    url = f"{API_HOST}/api/v1/web_search"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"query": query, "count": 5}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("data", {}).get("results", [])
        else:
            print(f"⚠️ Web search failed: {resp.status_code}")
            return []
    except Exception as e:
        print(f"⚠️ Web search error: {e}")
        return []


def generate_text(prompt: str) -> str:
    """Generate text using MiniMax API."""
    if not API_KEY:
        return ""

    url = f"{API_HOST}/api/v1/text/chatcompletion_v2"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.8,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            return (
                data.get("data", {})
                .get("choices", [{}])[0]
                .get("messages", [{}])[0]
                .get("content", "")
            )
        else:
            print(f"⚠️ Generate failed: {resp.status_code}")
            return ""
    except Exception as e:
        print(f"⚠️ Generate error: {e}")
        return ""


def generate_instagram_post(topic: str, trends: list) -> str:
    """Generate an Instagram post in Cantonese/Mandarin style."""
    if API_KEY:
        trends_text = "\n".join([f"- {t.get('title', t)}" for t in trends[:3]])
        prompt = f"""Generate an Instagram post about: {topic}

Trending related topics:
{trends_text}

Requirements:
- In Cantonese/Mixed Chinese (Yue + English hashtags)
- Casual, relatable tone
- Include emoji
- End with: #hashtags
- Max 300 characters
- Include product mention: Python Scripts Bundle $79 at everycompanyclaw.github.io
"""
        result = generate_text(prompt)
        if result:
            return result.strip()

    # Fallback
    posts = [
        """🤖 AI自動化管理公司｜你試過未？

用Python脚本自動化管理
省時慳力又高效

💰 $79 永久使用
⬇️ everycompanyclaw.github.io

#python #automation #hk #startup #ai #indiehacker""",

        """⚡ Build in Public 係咩體驗？

一邊做嘢一邊分享進度
建立個人品牌同時產品上線

👉 everycompanyclaw.github.io

#buildinpublic #startup #hongkong #sideproject #aibusiness""",
    ]
    import random

    return random.choice(posts)


def generate_threads_post(topic: str, trends: list) -> str:
    """Generate a Threads post in English."""
    if API_KEY:
        trends_text = "\n".join([f"- {t.get('title', t)}" for t in trends[:3]])
        prompt = f"""Generate a Threads post about: {topic}

Trending related topics:
{trends_text}

Requirements:
- In English
- Casual, entrepreneurial tone
- Include emoji
- End with relevant hashtags
- Max 500 characters
- Include: Products from $29 at everycompanyclaw.github.io
"""
        result = generate_text(prompt)
        if result:
            return result.strip()

    # Fallback
    posts = [
        """🚀 I built a company that runs itself 24/7

While I sleep, it:
- sells products automatically
- handles payments via Stripe
- ships digital goods instantly

Products from $29 → everycompanyclaw.github.io

#buildinpublic #startup #ai #automation #entrepreneur""",

        """💡 The best businesses scale without you

I used:
- AI agents to do the work
- Stripe for payments
- GitHub Pages for hosting
- OpenClaw to run it 24/7

$29 starter: everycompanyclaw.github.io

#passiveincome #automation #aibusiness #entrepreneur #startup""",
    ]
    import random

    return random.choice(posts)


def main():
    parser = argparse.ArgumentParser(description="Generate social media content with MiniMax")
    parser.add_argument("--topic", "-t", default="AI automation business", help="Topic to search and post about")
    parser.add_argument("--dry-run", action="store_true", help="Show content without saving")
    args = parser.parse_args()

    print(f"📡 MiniMax Content Generator")
    print(f"   Topic: {args.topic}")
    print(f"   API Key: {'✅ Set' if API_KEY else '❌ Not set (using fallback)'}")
    print()

    # Search for trends
    print(f"🔍 Searching: {args.topic}")
    trends = search_web(args.topic)
    print(f"   Found {len(trends)} trending items")

    # Generate posts
    print(f"\n✍️  Generating Instagram post...")
    ig_post = generate_instagram_post(args.topic, trends)
    print(f"\n📱 Instagram:\n{ig_post}")

    print(f"\n✍️  Generating Threads post...")
    threads_post = generate_threads_post(args.topic, trends)
    print(f"\n📘 Threads:\n{threads_post}")

    # Save to file for auto-poster
    output = {
        "generated_at": datetime.now().isoformat(),
        "topic": args.topic,
        "instagram": ig_post,
        "threads": threads_post,
    }
    path = "/tmp/company-automation/generated_posts.json"
    if not args.dry_run:
        with open(path, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Saved to {path}")
    else:
        print(f"\n🔎 [DRY RUN] Not saved")


if __name__ == "__main__":
    main()
