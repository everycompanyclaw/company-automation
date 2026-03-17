#!/usr/bin/env python3
"""
Social Media Auto-Poster
Sends ready-to-post content to Telegram for one-tap sharing
"""
import os

CONTENT_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/social_queue.md"

POSTS = [
    {
        "platform": "Instagram",
        "caption": """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用
⬇️ link in bio

#python #automation #hkig #香港 #startup #indiehacker""",
        "image": "ig-post.html"
    },
    {
        "platform": "Threads", 
        "caption": """🧵 我build咗一個自己運作既公司

佢會24/7自動賣嘢、收錢、發貨

products:
- Python腳本套裝 $79
- Zapier範本 $49
- AI提示詞 $29

link: everycompanyclaw.github.io/company-automation/

#buildinpublic #startup #香港""",
        "image": None
    },
    {
        "platform": "Twitter",
        "caption": """🧵 Built 20 Python scripts that automate repetitive tasks - saves 10+ hours/week

Email extractor, CSV converter, file organizer, invoice generator & more

$79 - instant download

👉 https://everycompanyclaw.github.io/company-automation/

#automation #python #buildinpublic""",
        "image": None
    }
]

def get_next_post():
    """Get next post to share"""
    if POSTS:
        return POSTS[0]
    return None

def generate_telegram_message(post):
    """Generate message for Telegram"""
    msg = f"""📱 *{post['platform']} Post Ready*

{post['caption']}

---
Copy and post!"""
    return msg

if __name__ == "__main__":
    post = get_next_post()
    if post:
        print(generate_telegram_message(post))
