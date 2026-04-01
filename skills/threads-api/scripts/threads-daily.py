#!/usr/bin/env python3
"""Threads Auto-Poster with AI-Generated Content + MiniMax Images — Daily 6pm"""

import json
import random
import re
import requests
import time
from pathlib import Path
from datetime import datetime

CONFIG_DIR = Path("/Users/macbookpro/.openclaw/company/.config")
TOKEN_FILE = CONFIG_DIR / "threads-token.enc"
USER_ID = "26139168152370559"

MINIMAX_KEY = "sk-cp-8uTKtvqWkjFq9d1OD7l5-27BpbbbKyJcnJ8u0ftdMeXjNrqBk7tFhfvN-ihocizUg5qiputqB__kXnM0EO0ksT2_79YOHLTDvJFEGceJApOs82QOOY8MBHM"
MINIMAX_IMG_URL = "https://api.minimaxi.com/v1/image_generation"
MINIMAX_TEXT_URL = "https://api.minimaxi.com/v1/chat/completions"

CAT_PERSONAS = [
    "serious businessman cat in a suit working at a standing desk",
    "chill cat lounging in a minimalist Hong Kong apartment",
    "curious cat exploring a neon-lit Kowloon street at night",
    "productive cat with laptop and coffee at a cozy cafe",
    "wise cat reading financial news with glasses",
    "playful cat in a robot costume representing AI future",
    "relaxed cat enjoying dim sum with pandas",
    "fashionable cat at a rooftop bar overlooking the harbour",
    "studious cat surrounded by code and books",
    "zen cat meditating in a bamboo forest",
]

TOPIC_HINTS = [
    "lifestyle and productivity tips for busy Hong Kong professionals",
    "fun and humorous everyday observations about work and life",
    "financial wisdom and investing concepts for beginners",
    "automation and AI tools that save time and make money",
]

def load_token():
    with open(TOKEN_FILE) as f:
        return f.read().strip()

def generate_content_with_ai(topic_hint: str) -> str:
    prompt = f"""你係EveryCompanyClaw嘅社交媒體內容創作者。

請為Threads創作一篇最多140字嘅繁體中文帖子，風格輕鬆有趣，適合香港讀者。

主題：{topic_hint}

要求：
- 最多140字
- 繁體中文
- 輕鬆有趣嘅語氣
- 適合香港打工仔
- 結尾加2-3個相關hashtags（英文）
- 直接輸出帖子內容，唔好加任何解釋或思考過程

立即輸出："""

    headers = {
        "Authorization": f"Bearer {MINIMAX_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "MiniMax-M2.7",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 250,
        "temperature": 0.8
    }
    
    try:
        resp = requests.post(MINIMAX_TEXT_URL, headers=headers, json=data, timeout=30)
        result = resp.json()
        raw = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        
        # Remove thinking tags and extra whitespace
        content = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
        content = re.sub(r'\s+', ' ', content)
        
        if content and len(content) <= 500:
            return content
        elif content:
            return content[:500]
    except Exception as e:
        print(f"⚠️ Text gen error: {e}")
    
    return None

def generate_image_minimax(persona: str) -> str:
    prompt = f"Pixar Disney style 3D animated cat character, {persona}, big expressive eyes, beautiful lighting, Disney Pixar animation quality, volumetric lighting, highly detailed fur"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": "1:1"
    }
    
    resp = requests.post(MINIMAX_IMG_URL, headers=headers, json=data, timeout=60)
    result = resp.json()
    
    if result.get("base_resp", {}).get("status_code") == 0:
        image_urls = result.get("data", {}).get("image_urls", [])
        if image_urls:
            return image_urls[0]
    
    print(f"⚠️ Image gen failed: {result}")
    return None

def post_with_image_url(token: str, image_url: str, text: str) -> dict:
    """Post with image - Two step process"""
    # Step 1: Create container
    url = f"https://graph.threads.net/v1.0/{USER_ID}/threads"
    data = {
        "access_token": token,
        "media_type": "image",
        "image_url": image_url,
        "text": text
    }
    resp = requests.post(url, json=data)
    result = resp.json()
    
    if 'id' not in result:
        return result
    
    # Step 2: Publish
    time.sleep(1)
    publish_url = f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish"
    publish_data = {"access_token": token, "creation_id": result['id']}
    publish_resp = requests.post(publish_url, json=publish_data)
    return publish_resp.json()

def post_text_only(token: str, text: str) -> dict:
    """Post text only - Two step process"""
    # Step 1: Create container
    url = f"https://graph.threads.net/v1.0/{USER_ID}/threads"
    data = {
        "access_token": token,
        "media_type": "text",
        "text": text
    }
    resp = requests.post(url, json=data)
    result = resp.json()
    
    if 'id' not in result:
        return result
    
    # Step 2: Publish
    time.sleep(1)
    publish_url = f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish"
    publish_data = {"access_token": token, "creation_id": result['id']}
    publish_resp = requests.post(publish_url, json=publish_data)
    return publish_resp.json()

def main():
    topic_hint = random.choice(TOPIC_HINTS)
    persona = random.choice(CAT_PERSONAS)
    
    print(f"🎲 Topic: {topic_hint[:40]}... | Persona: {persona[:40]}...")
    
    token = load_token()
    
    print("✍️ Generating unique content with AI...")
    content = generate_content_with_ai(topic_hint)
    
    if not content:
        content = f"EveryCompanyClaw running 24/7 so you don't have to.\n\n#automation #AI #business"
    
    print(f"📝 Content: {content[:100]}...")
    print(f"📏 Length: {len(content)} chars")
    
    print("🎨 Generating image with MiniMax...")
    image_url = generate_image_minimax(persona)
    
    # Only use image if URL is a proper HTTP URL (not base64 data URL)
    if image_url and image_url.startswith('http'):
        print(f"📸 Posting with image...")
        result = post_with_image_url(token, image_url, content)
        if 'error' in result:
            print(f"⚠️ Image post failed, falling back to text...")
            result = post_text_only(token, content)
    else:
        print("📝 Posting text only...")
        result = post_text_only(token, content)
    
    if 'id' in result:
        print(f"✅ Posted! ID: {result['id']}")
    else:
        print(f"❌ Error: {result}")
    
    print(f"[{datetime.now()}] Done")

if __name__ == "__main__":
    main()
