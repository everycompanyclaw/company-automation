#!/usr/bin/env python3
"""
Get real Instagram stats via API
"""
import requests
import json

TOKEN = "IGAAU3w4V9XB5BZAGFqLWlKT2twUW5FSk45UGZABLTRnMllkZAlRQSkNsVE5GZATF5dlNwSUNJZA0FDVlRDOVF3bE5iUWtRd2hmQUpiRFBoX05GRkU2OXBuQWFlYW5DZAHdrV1ZAiekZArSU5DdmxuTWZAuYUFxVFk0Nk5xeWY1UkktS18zcwZDZD"

def get_instagram_stats():
    """Fetch real Instagram media and stats"""
    # Get user media
    url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,permalink,timestamp,like_count,comments_count&access_token={TOKEN}&limit=10"
    r = requests.get(url)
    data = r.json()
    
    posts = []
    for item in data.get("data", []):
        posts.append({
            "platform": "Instagram",
            "content": item.get("caption", "")[:100],
            "link": item.get("permalink", ""),
            "posted": item.get("timestamp", "")[:10],
            "reach": item.get("like_count", 0) * 10,  # Approximate
            "likes": item.get("like_count", 0),
            "comments": item.get("comments_count", 0)
        })
    
    return posts

if __name__ == "__main__":
    posts = get_instagram_stats()
    print(f"Found {len(posts)} posts")
    for p in posts:
        print(f"  - {p['posted']}: {p['content'][:50]}...")
