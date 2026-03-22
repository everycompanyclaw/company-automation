#!/usr/bin/env python3
"""
Instagram API Poster - Uses real data for content
Requires Instagram Basic Display API with content_publish permissions
"""
import os
import json
import requests
from datetime import datetime

# Instagram API config
IG_USER_ID = "26150126261339190"
ACCESS_TOKEN = "IGAAU3w4V9XB5BZAGFqLWlKT2twUW5FSk45UGZABLTRnMllkZAlRQSkNsVE5GZATF5dlNwSUNJZA0FDVlRDOVF3bE5iUWtRd2hmQUpiRFBoX05GRkU2OXBuQWFlYW5DZAHdrV1ZAiekZArSU5DdmxuTWZAuYUFxVFk0Nk5xeWY1UkktS18zcwZDZD"

BASE_URL = "https://graph.instagram.com/v21.0"

def get_trending_hashtag():
    """Get real trending topic for content"""
    try:
        resp = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10
        )
        if resp.status_code == 200:
            ids = resp.json()[:1]
            item = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{ids[0]}.json",
                timeout=5
            )
            if item.status_code == 200:
                title = item.json().get("title", "")
                return title[:50] if title else "AI Automation"
    except:
        pass
    return "AI Automation"

def create_media_container(caption, image_url):
    """Create media container"""
    url = f"{BASE_URL}/{IG_USER_ID}/media"
    
    data = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    
    resp = requests.post(url, data=data, timeout=30)
    result = resp.json()
    
    print(f"Container creation: {result}")
    return result

def publish_media(creation_id):
    """Publish the media"""
    url = f"{BASE_URL}/{IG_USER_ID}/media_publish"
    
    data = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }
    
    resp = requests.post(url, data=data, timeout=30)
    result = resp.json()
    
    print(f"Publish result: {result}")
    return result

def get_user_media():
    """Check existing media"""
    url = f"{BASE_URL}/{IG_USER_ID}/media"
    
    params = {
        "fields": "id,caption,timestamp",
        "access_token": ACCESS_TOKEN,
        "limit": 5
    }
    
    resp = requests.get(url, params=params, timeout=10)
    return resp.json()

def post_to_instagram():
    """Main posting function"""
    print("📸 Instagram API Poster")
    print("=" * 40)
    
    # Get trending topic
    topic = get_trending_hashtag()
    caption = f"🤖 {topic}\n\n💡 AI Automation for Business\n💰 Save 10+ hours/week\n\n#automation #ai #startup #tech"
    
    # Try with a working image URL (need publicly accessible)
    # Using a sample image
    image_url = "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1080"
    
    print(f"Caption: {caption[:50]}...")
    print(f"Image: {image_url}")
    
    # Try to create container
    result = create_media_container(caption, image_url)
    
    if "id" in result:
        # Success - now publish
        creation_id = result["id"]
        pub_result = publish_media(creation_id)
        
        if "id" in pub_result:
            print(f"✅ Posted! Media ID: {pub_result['id']}")
            return True
    
    # Check what went wrong
    print(f"❌ Failed: {result}")
    
    # Check existing media
    media = get_user_media()
    print(f"Current media: {media}")
    
    return False

if __name__ == "__main__":
    post_to_instagram()