#!/usr/bin/env python3
"""
Social Media Scheduler - Schedule posts for later
Prepares posts that can be scheduled via Buffer/Later
"""
import os
import json
from datetime import datetime, timedelta

SCHEDULE_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/scheduled_posts.json"

POSTS = [
    {
        "platform": "Instagram",
        "content": """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker""",
        "image": "python-scripts.png",
        "scheduled": False
    },
    {
        "platform": "Instagram", 
        "content": """🤖 我build咗一個AI公司

24/7自動運作
自動賣產品、收錢、發貨

$79起｜everycompanyclaw.github.io

#buildinpublic #automation #ai""",
        "image": None,
        "scheduled": False
    },
    {
        "platform": "Threads",
        "content": """日頭寫code
夜晚瞓覺
一樣有收入

呢個就係自動化既威力

👉 everycompanyclaw.github.io/company-automation/

#automation #passiveincome #sideproject""",
        "image": None,
        "scheduled": False
    },
    {
        "platform": "Twitter",
        "content": """🧵 Built 20 Python scripts that automate repetitive tasks - saves 10+ hours/week

Email extractor, CSV converter, file organizer, invoice generator & more

$79 - instant download

👉 https://everycompanyclaw.github.io/company-automation/

#automation #python #buildinpublic""",
        "image": None,
        "scheduled": False
    }
]

def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE) as f:
            return json.load(f)
    return {"posts": POSTS, "last_updated": datetime.now().isoformat()}

def save_schedule(data):
    data["last_updated"] = datetime.now().isoformat()
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_next_post():
    """Get next unscheduled post"""
    data = load_schedule()
    for post in data["posts"]:
        if not post.get("scheduled"):
            return post
    return None

def schedule_post(post_id):
    """Mark a post as scheduled"""
    data = load_schedule()
    if 0 <= post_id < len(data["posts"]):
        data["posts"][post_id]["scheduled"] = True
        data["posts"][post_id]["scheduled_at"] = datetime.now().isoformat()
        save_schedule(data)
        return True
    return False

def generate_buffer_format():
    """Generate posts in Buffer API format"""
    data = load_schedule()
    
    buffer_posts = []
    for i, post in enumerate(data["posts"]):
        if not post.get("scheduled"):
            buffer_posts.append({
                "text": post["content"],
                "platform": post["platform"]
            })
    
    return buffer_posts

def main():
    print("""
📅 Social Media Scheduler
=======================

Options:
1. View scheduled posts
2. Get next post for Instagram
3. Mark post as scheduled
4. Generate for Buffer API
""")
    
    data = load_schedule()
    
    print(f"\n📋 Total posts: {len(data['posts'])}")
    print(f"✅ Scheduled: {sum(1 for p in data['posts'] if p.get('scheduled'))}")
    print(f"⏳ Pending: {sum(1 for p in data['posts'] if not p.get('scheduled'))}")
    
    next_post = get_next_post()
    if next_post:
        print(f"\n📝 Next post ({next_post['platform']}):")
        print("-" * 40)
        print(next_post["content"])
        print("-" * 40)

if __name__ == "__main__":
    main()
