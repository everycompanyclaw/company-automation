#!/usr/bin/env python3
"""
Instagram Auto-Post via Facebook GraphQL API
"""
import requests
import os
import json

# Configuration
FB_PAGE_ID = os.environ.get("FB_PAGE_ID", "")
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN", "")
IG_BUSINESS_ID = os.environ.get("IG_BUSINESS_ID", "")

# Facebook GraphQL endpoints
FB_API = "https://graph.facebook.com/v18.0"
IG_API = "https://graph.facebook.com/v18.0"

def get_ig_business_account():
    """Get connected Instagram Business account"""
    if not FB_ACCESS_TOKEN:
        return {"error": "No access token"}
    
    url = f"{FB_API}/{FB_PAGE_ID}?fields=instagram_business_account&access_token={FB_ACCESS_TOKEN}"
    r = requests.get(url)
    return r.json()

def post_to_ig_image(message, image_url=None):
    """Post image to Instagram"""
    if not IG_BUSINESS_ID or not FB_ACCESS_TOKEN:
        return {"error": "Missing credentials"}
    
    # Create media container
    url = f"{IG_API}/{IG_BUSINESS_ID}/media"
    data = {
        "image_url": image_url,
        "caption": message,
        "access_token": FB_ACCESS_TOKEN
    }
    
    r = requests.post(url, data=data)
    container = r.json()
    
    if "id" in container:
        # Publish the container
        publish_url = f"{IG_API}/{IG_BUSINESS_ID}/media_publish"
        publish_data = {
            "creation_id": container["id"],
            "access_token": FB_ACCESS_TOKEN
        }
        r2 = requests.post(publish_url, data=publish_data)
        return r2.json()
    
    return container

def post_to_ig_carousel(message, image_urls):
    """Post carousel to Instagram"""
    if not IG_BUSINESS_ID or not FB_ACCESS_TOKEN:
        return {"error": "Missing credentials"}
    
    # Create children media
    children = []
    for i, url in enumerate(image_urls):
        url_api = f"{IG_API}/{IG_BUSINESS_ID}/media"
        data = {
            "image_url": url,
            "is_carousel_item": True,
            "access_token": FB_ACCESS_TOKEN
        }
        r = requests.post(url_api, data=data)
        children.append(r.json().get("id"))
    
    # Create carousel container
    carousel_url = f"{IG_API}/{IG_BUSINESS_ID}/media"
    carousel_data = {
        "media_type": "CAROUSEL",
        "caption": message,
        "carousel_media": [{"media_id": cid} for cid in children],
        "access_token": FB_ACCESS_TOKEN
    }
    r = requests.post(carousel_url, data=carousel_data)
    container = r.json()
    
    if "id" in container:
        publish_url = f"{IG_API}/{IG_BUSINESS_ID}/media_publish"
        publish_data = {
            "creation_id": container["id"],
            "access_token": FB_ACCESS_TOKEN
        }
        r2 = requests.post(publish_url, data=publish_data)
        return r2.json()
    
    return container

def post_ig(message, image_url=None):
    """Main posting function"""
    print("📸 Instagram GraphQL Post")
    print("=" * 40)
    
    if not FB_ACCESS_TOKEN:
        print("❌ No access token!")
        print("\nTo get credentials:")
        print("1. Go to developers.facebook.com")
        print("2. Create app with Instagram Basic Display")
        print("3. Add Instagram Graph API")
        print("4. Get Page Access Token")
        print("\nSet environment:")
        print("  FB_PAGE_ID=your_page_id")
        print("  FB_ACCESS_TOKEN=your_token")
        print("  IG_BUSINESS_ID=your_ig_business_id")
        return {"error": "no_credentials"}
    
    # Get IG account
    ig_account = get_ig_business_account()
    print(f"IG Account: {ig_account}")
    
    # Post
    if image_url:
        result = post_to_ig_image(message, image_url)
    else:
        result = {"error": "Need image_url for now"}
    
    print(f"Result: {result}")
    return result

if __name__ == "__main__":
    # Test post
    test_message = "🧠 Testing Instagram API posting from EveryCompanyClaw! #AI #automation"
    
    result = post_ig(test_message)
    print(json.dumps(result, indent=2))
