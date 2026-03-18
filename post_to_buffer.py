#!/usr/bin/env python3
"""
Buffer Integration - Auto-post to Buffer, Buffer posts to Instagram
Set BUFFER_ACCESS_TOKEN to use
"""
import os
import requests
import json
from datetime import datetime

BUFFER_API = "https://api.bufferapp.com/1"

# Set your Buffer access token
BUFFER_ACCESS_TOKEN = os.environ.get('BUFFER_ACCESS_TOKEN', '')

POSTS = [
    {
        "text": """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker""",
        "platforms": ["instagram"]
    },
    {
        "text": """🤖 我build咗一個AI公司

24/7自動運作
自動賣產品、收錢、發貨

$79起｜everycompanyclaw.github.io

#buildinpublic #automation #ai""",
        "platforms": ["instagram"]
    },
    {
        "text": """🧵 Built 20 Python scripts that automate repetitive tasks

$79 - instant download

👉 https://everycompanyclaw.github.io/company-automation/

#automation #python #buildinpublic""",
        "platforms": ["twitter"]
    }
]

def get_profiles():
    """Get connected social profiles"""
    if not BUFFER_ACCESS_TOKEN:
        return None
    
    url = f"{BUFFER_API}/profiles.json?access_token={BUFFER_ACCESS_TOKEN}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

def schedule_post(text, platforms=None):
    """Schedule a post via Buffer"""
    if not BUFFER_ACCESS_TOKEN:
        return {"error": "No Buffer access token"}
    
    url = f"{BUFFER_API}/updates/create.json"
    
    data = {
        "access_token": BUFFER_ACCESS_TOKEN,
        "text": text,
    }
    
    if platforms:
        # Add profiles for each platform
        profiles = get_profiles()
        if profiles:
            profile_ids = [p["id"] for p in profiles if p["service"] in platforms]
            data["profile_ids"] = profile_ids
    
    r = requests.post(url, data=data)
    return r.json() if r.status_code == 200 else r.json()

def auto_post_to_buffer():
    """Auto-post next available post to Buffer"""
    for post in POSTS:
        result = schedule_post(post["text"], post.get("platforms"))
        print(f"Posted to {post.get('platforms', 'all')}: {result}")
        
        if "error" not in result:
            break

def main():
    print("""
📅 Buffer Auto-Poster
=====================

To use:
1. Get Buffer access token: https://buffer.com/developers
2. Set: export BUFFER_ACCESS_TOKEN='your_token'
3. Connect Instagram to Buffer
4. Run this script!

Current status: {}
""".format("✅ Connected" if BUFFER_ACCESS_TOKEN else "❌ Need Token"))
    
    if BUFFER_ACCESS_TOKEN:
        profiles = get_profiles()
        if profiles:
            print(f"\n✅ Connected profiles:")
            for p in profiles:
                print(f"  - {p['service']}: {p['formatted_username']}")
            
            print("\n🚀 Ready to auto-post!")
            print("Run: python3 post_to_buffer.py")
        else:
            print("\n⚠️ No profiles connected in Buffer")

if __name__ == "__main__":
    main()
