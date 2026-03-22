#!/usr/bin/env python3
"""
Social Poster - saves posts to JSON
"""
import json
import os
from datetime import datetime

POSTS_FILE = "/tmp/real_posts.json"

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "r") as f:
            return json.load(f)
    return {"posts": []}

def save_posts(posts):
    with open(POSTS_FILE, "w") as f:
        json.dump(posts, f, indent=2)

def add_post(platform, content, link=""):
    posts = load_posts()
    posts["posts"].insert(0, {
        "id": len(posts["posts"]) + 1,
        "platform": platform,
        "content": content,
        "link": link,
        "posted": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "reach": 0,
        "likes": 0,
        "comments": 0
    })
    save_posts(posts)
    print(f"✅ Added {platform} post")

# Demo - add your recent post
if __name__ == "__main__":
    add_post(
        "Instagram", 
        "🧵 20 Python自動化腳本｜幫你慳10+粒鐘 由Email提取器、檔案整理器、發票生成器... 全部已經寫好，等你去用！ 💰 $79 = 永久使用 ⬇️ link in bio #python #automation #hkig #香港 #startup #indiehacker",
        "https://instagram.com/p/your_post_id"
    )
