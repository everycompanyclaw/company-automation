#!/usr/bin/env python3
"""
Instagram Post Scheduler
Schedule and auto-post content to Instagram
"""
import os
import time
import json
from datetime import datetime, timedelta

# Config
POSTS_FILE = "instagram_posts.json"
MEDIA_FOLDER = "instagram_media"

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(POSTS_FILE, "w") as f:
        json.dump(posts, f, indent=2)

def add_post(caption, image_path, scheduled_time=None):
    """Add a post to the schedule"""
    posts = load_posts()
    
    post = {
        "id": len(posts) + 1,
        "caption": caption,
        "image": image_path,
        "scheduled": scheduled_time or datetime.now().isoformat(),
        "status": "pending"
    }
    
    posts.append(post)
    save_posts(posts)
    return post

def get_pending_posts():
    """Get posts ready to post"""
    posts = load_posts()
    now = datetime.now()
    
    ready = []
    for p in posts:
        if p["status"] == "pending":
            scheduled = datetime.fromisoformat(p["scheduled"])
            if scheduled <= now:
                ready.append(p)
    
    return ready

def post_to_instagram(post):
    """Post to Instagram (using instagrapi)"""
    # This would use instagrapi library
    # from instagrapi import Client
    # client = Client()
    # client.login(username, password)
    # client.photo_upload(post["image"], post["caption"])
    
    print(f"Would post: {post['caption']}")
    print(f"Image: {post['image']}")
    
    # Mark as posted
    posts = load_posts()
    for p in posts:
        if p["id"] == post["id"]:
            p["status"] = "posted"
            p["posted_at"] = datetime.now().isoformat()
    
    save_posts(posts)
    return True

def check_and_post():
    """Check for pending posts and post them"""
    pending = get_pending_posts()
    
    for post in pending:
        print(f"Posting: {post['caption'][:50]}...")
        post_to_instagram(post)
    
    return len(pending)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "add":
            caption = sys.argv[2] if len(sys.argv) > 2 else "Auto post"
            image = sys.argv[3] if len(sys.argv) > 3 else "image.jpg"
            add_post(caption, image)
            print("Post added!")
        
        elif sys.argv[1] == "check":
            n = check_and_post()
            print(f"Posted {n} posts")
        
        elif sys.argv[1] == "list":
            posts = load_posts()
            for p in posts:
                print(f"{p['id']}. {p['caption'][:30]}... - {p['status']}")
    else:
        print("Usage:")
        print("  python instagram_scheduler.py add 'caption' 'image.jpg'")
        print("  python instagram_scheduler.py check")
        print("  python instagram_scheduler.py list")
