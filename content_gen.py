#!/usr/bin/env python3
"""
Content Generator - Generate multiple posts
"""
import random

TOPICS = [
    "AI自動化",
    "香港創業",
    "網店经营",
    "數碼轉型",
    "營銷技巧",
    "賺錢方法",
    "科技趨勢",
    "Freelance"
]

CAPTIONS = [
    "你試過未?",
    "一定要知!",
    "懶人必看",
    "老闆必讀",
    "2026趨勢",
    "唔好錯過",
    "實用技巧",
    "立即行動"
]

def generate_post():
    topic = random.choice(TOPICS)
    caption = random.choice(CAPTIONS)
    
    return f"""🚀 {topic} - {caption}

{topic}可以點幫到你既business?
DM我傾下!

#hk #startup #business #automation #ai"""

def main():
    posts = [generate_post() for _ in range(3)]
    for i, p in enumerate(posts, 1):
        print(f"\n=== Post {i} ===")
        print(p)

if __name__ == "__main__":
    main()
