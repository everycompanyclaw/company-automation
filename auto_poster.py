#!/usr/bin/env python3
"""
Auto-Poster for Instagram/TikTok
Ready to post when you add credentials
"""
import os
import json
from datetime import datetime

POSTS_FILE = "scheduled_posts.json"

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "r") as f:
            return json.load(f)
    return []

def add_post(video_file, caption, scheduled_date, platform="instagram"):
    posts = load_posts()
    post = {
        "id": len(posts) + 1,
        "video": video_file,
        "caption": caption,
        "platform": platform,
        "scheduled": scheduled_date,
        "status": "ready",
        "created": datetime.now().isoformat()
    }
    posts.append(post)
    with open(POSTS_FILE, "w") as f:
        json.dump(posts, f, indent=2)
    return post

def get_ready_posts():
    posts = load_posts()
    now = datetime.now().strftime("%Y-%m-%d")
    ready = [p for p in posts if p["scheduled"] <= now and p["status"] == "ready"]
    return ready

# Add scheduled posts
posts = [
    ("video1.mp4", """Hey everyone! In this video, I'm going to show you how to save 10 hours every single week using Python automation.

First, think about all the repetitive tasks you do every day...

Second, here's the secret - Python can do all of this automatically.

Third, the best part? It runs while I sleep!

#Python #Automation #Productivity #Tech""", "2026-03-19"),
    
    ("video2.mp4", """AI tools that actually work in 2026!

Number 1: ChatGPT for writing
Number 2: Claude for coding
Number 3: Python + APIs

Which AI tool is your favorite?

#AI #ChatGPT #Claude #Productivity""", "2026-03-21"),
    
    ("video3.mp4", """Let me tell you how I built a freelance business from scratch...

It started when I realized I was spending 10 hours on manual tasks every week.

Then I learned Python. I built my first automation script.

The secret: learn one skill, automate, grow.

#Freelance #Python #SideHustle #Business""", "2026-03-23")
]

for video, caption, date in posts:
    add_post(video, caption, date)

print("✅ Added 3 posts to schedule!")

# Show posts
for p in load_posts():
    print(f"Post {p['id']}: {p['scheduled']} - {p['status']}")
