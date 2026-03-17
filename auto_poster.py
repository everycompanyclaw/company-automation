#!/usr/bin/env python3
"""
Auto Social Poster - Output to stdout (for Telegram)
Runs every 6 hours
"""
import os
import json
from datetime import datetime

POST_INDEX_FILE = "/Users/macbookpro/.openclaw/workspace/company/automation/data/post_index.json"

POSTS = [
    {
        "platform": "Instagram",
        "content": """🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用
⬇️ link in bio

#python #automation #hkig #香港 #startup #indiehacker"""
    },
    {
        "platform": "Threads", 
        "content": """🧵 我build咗一個自己運作既公司

佢會24/7自動賣嘢、收錢、發貨

products:
- Python腳本套裝 $79
- Zapier範本 $49
- AI提示詞 $29

link: everycompanyclaw.github.io/company-automation/

#buildinpublic #startup #香港"""
    },
    {
        "platform": "Twitter",
        "content": """🧵 Built 20 Python scripts that automate repetitive tasks - saves 10+ hours/week

Email extractor, CSV converter, file organizer, invoice generator & more

$79 - instant download

👉 https://everycompanyclaw.github.io/company-automation/

#automation #python #buildinpublic"""
    },
    {
        "platform": "WhatsApp Business",
        "content": """🤖 Python Scripts Bundle - $79

20個自動化腳本：
- Email提取器
- 檔案整理器
- 發票生成器
- CSV/JSON轉換
- 仲有更多...

即時下載：everycompanyclaw.github.io/company-automation/

#automation #python #香港"""
    }
]

def load_index():
    if os.path.exists(POST_INDEX_FILE):
        with open(POST_INDEX_FILE) as f:
            return json.load(f)
    return {"index": 0}

def save_index(idx):
    with open(POST_INDEX_FILE, "w") as f:
        json.dump({"index": idx}, f)

def get_next_post():
    data = load_index()
    idx = data.get("index", 0)
    post = POSTS[idx % len(POSTS)]
    return post, idx

def auto_post():
    """Generate next post content"""
    post, idx = get_next_post()
    
    message = f"""📱 *Ready to Post - {post['platform']}*

{post['content']}

---
Copy → Paste → Done! ✅"""
    
    print(message)
    
    # Save next index
    save_index(idx + 1)
    
    return True

if __name__ == "__main__":
    print(f"🚀 Auto Social Poster - {datetime.now()}\n")
    auto_post()
