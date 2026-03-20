#!/usr/bin/env python3
"""
Auto Instagram Scheduler - Posts to Telegram, you forward to IG
Runs every 6 hours via cron
"""
import os
import json
from datetime import datetime

SCHEDULE_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/ig_schedule.json"

POSTS = [
    {
        "content": """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker""",
        "posted": False,
        "scheduled_time": None
    },
    {
        "content": """🤖 我build咗一個AI公司

24/7自動運作
自動賣產品、收錢、發貨

$79起｜everycompanyclaw.github.io

#buildinpublic #automation #ai""",
        "posted": False,
        "scheduled_time": None
    },
    {
        "content": """💰 Python Scripts Bundle

20個自動化腳本：
- Email提取器
- 檔案整理器
- 發票生成器
- CSV/JSON轉換
- 仲有更多...

$79 即時下載

everycompanyclaw.github.io

#automation #python #香港""",
        "posted": False,
        "scheduled_time": None
    },
    {
        "content": """🚀 Build in public

AI公司運行中...

Products:
- Python Scripts $79
- Zapier Templates $49
- AI Prompts $29

everycompanyclaw.github.io

#indiehacker #startup #automation""",
        "posted": False,
        "scheduled_time": None
    }
]

def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE) as f:
            return json.load(f)
    return {"posts": POSTS, "last_check": datetime.now().isoformat()}

def save_schedule(data):
    data["last_check"] = datetime.now().isoformat()
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_next_post():
    data = load_schedule()
    for post in data["posts"]:
        if not post.get("posted"):
            return post
    # Reset if all posted
    for post in data["posts"]:
        post["posted"] = False
    save_schedule(data)
    return data["posts"][0]

def mark_posted():
    data = load_schedule()
    for post in data["posts"]:
        if not post.get("posted"):
            post["posted"] = True
            post["posted_at"] = datetime.now().isoformat()
            save_schedule(data)
            return True
    return False

def main():
    print("📅 Instagram Scheduler Check")
    
    post = get_next_post()
    
    print(f"""
🎯 Next Post Ready:

{post['content']}

---
Copy → Paste to Instagram → Done!

""")
    
    # Don't auto-mark as posted - user must confirm
    # mark_posted()  # Uncomment to auto-mark after running

if __name__ == "__main__":
    main()
