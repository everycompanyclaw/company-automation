#!/usr/bin/env python3
"""
Video Content Generator
Creates scripts and content for social media videos
"""
import os
import json
from datetime import datetime

CONTENT_FILE = "video_content.json"
MEDIA_FOLDER = "video_media"

def load_content():
    if os.path.exists(CONTENT_FILE):
        with open(CONTENT_FILE, "r") as f:
            return json.load(f)
    return []

def save_content(content):
    with open(CONTENT_FILE, "w") as f:
        json.dump(content, f, indent=2)

def generate_script(topic, style="educational"):
    """Generate video script"""
    
    templates = {
        "educational": {
            "intro": f"Hey everyone! Today we're talking about {topic}",
            "body": [
                f"Let me share 3 key points about {topic}:",
                "First, ",
                "Second, ",
                "And finally, "
            ],
            "outro": "Subscribe for more!"
        },
        "short": {
            "intro": f"{topic} in 60 seconds!",
            "body": [
                "Point 1: ",
                "Point 2: ",
                "Point 3: "
            ],
            "outro": "Like & follow!"
        },
        "story": {
            "intro": "Let me tell you a story about something amazing...",
            "body": [
                "It started when ",
                "Then something unexpected happened: ",
                "The result was incredible: "
            ],
            "outro": "What do you think? Let me know!"
        }
    }
    
    return templates.get(style, templates["educational"])

def create_video_content(title, topic, style="educational", hashtags=None):
    """Create new video content"""
    content = load_content()
    
    script = generate_script(topic, style)
    
    video = {
        "id": len(content) + 1,
        "title": title,
        "topic": topic,
        "style": style,
        "script": script,
        "hashtags": hashtags or ["#automation", "#tech", "#hongkong"],
        "status": "draft",
        "created": datetime.now().isoformat(),
        "platform": []
    }
    
    content.append(video)
    save_content(content)
    
    return video

def get_drafts():
    """Get all draft content"""
    content = load_content()
    return [c for c in content if c["status"] == "draft"]

def mark_ready(video_id, platform):
    """Mark video as ready for platform"""
    content = load_content()
    for c in content:
        if c["id"] == video_id:
            c["status"] = "ready"
            c["platform"].append(platform)
    save_content(content)

# Example topics for company
COMPANY_TOPICS = [
    ("Save 10 Hours/Week with Python Automation", "educational"),
    ("AI Tools That Actually Work", "short"),
    ("How I Built a Freelance Business", "story"),
    ("Python Script in 60 Seconds", "short"),
    ("The Future of Work is Remote", "educational")
]

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "create":
            title = sys.argv[2] if len(sys.argv) > 2 else "New Video"
            topic = sys.argv[3] if len(sys.argv) > 3 else "Automation"
            style = sys.argv[4] if len(sys.argv) > 4 else "educational"
            v = create_video_content(title, topic, style)
            print(f"Created: {v['title']}")
            print(f"Script: {v['script']['intro']}")
        
        elif sys.argv[1] == "list":
            drafts = get_drafts()
            print(f"Drafts: {len(drafts)}")
            for d in drafts:
                print(f"  - {d['title']} ({d['style']})")
        
        elif sys.argv[1] == "generate-company":
            for title, style in COMPANY_TOPICS:
                create_video_content(title, title, style)
            print("Generated 5 company videos!")
    else:
        print("Usage:")
        print("  python video_content.py create 'Title' 'topic' 'style'")
        print("  python video_content.py list")
        print("  python video_content.py generate-company")
