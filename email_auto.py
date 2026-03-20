#!/usr/bin/env python3
"""
Email Automation - Weekly newsletter/content
"""
from datetime import datetime

SUBJECTS = [
    "AI幫你慳咗幾多時間?",
    "呢個禮拜既科技趨勢",
    "自動化 tip你可以立即用",
    "中小企既數碼轉型之路",
    "你需要既5個AI工具"
]

CONTENT_PREVIEW = """
呢排AI既發展真係快!
如果你有咩問題，歡迎回覆傾下!
- EveryCompany Team
"""

def generate_email():
    """Generate email content"""
    import random
    subject = random.choice(SUBJECTS)
    return subject, CONTENT_PREVIEW

def main():
    print("📧 Email Automation")
    subject, content = generate_email()
    print(f"Subject: {subject}")
    print(f"Preview: {content}")

if __name__ == "__main__":
    main()
