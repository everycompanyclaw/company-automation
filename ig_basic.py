#!/usr/bin/env python3
"""
Instagram Basic Display API Auto-Post
"""
import requests
import os
import json

# User provided credentials
IG_APP_ID = "1468687781288990"
IG_ACCESS_TOKEN = "IGAAU3w4V9XB5BZAFo5U1JLaF9kUTZAfRTE3S1dPRjJLVGlGWV83WWpKRXpscmJPcElnUDFTS3ZAXUndObTR4QWtqSDFaeTljTDlGXzVTWjN2dHZATdlJfQXZAlcjk3eXRzRlNjemVldEQwLWxBckYxeU5ZAS0dnSkI4R1IwRDdSdVp6bwZDZD"

# Instagram Basic Display API
IG_API = "https://graph.instagram.com"

def get_ig_user():
    """Get Instagram user info"""
    url = f"{IG_API}/me?fields=id,username,media_count,account_type&access_token={IG_ACCESS_TOKEN}"
    r = requests.get(url)
    return r.json()

def post_image(caption, image_url):
    """Post image to Instagram"""
    # Create media container
    url = f"{IG_API}/me/media"
    data = {
        "image_url": image_url,
        "caption": caption,
        "access_token": IG_ACCESS_TOKEN
    }
    r = requests.post(url, data=data)
    result = r.json()
    print(f"Create media: {result}")
    
    if "id" in result:
        # Publish the media
        publish_url = f"{IG_API}/me/media_publish"
        publish_data = {
            "creation_id": result["id"],
            "access_token": IG_ACCESS_TOKEN
        }
        r2 = requests.post(publish_url, data=publish_data)
        return r2.json()
    
    return result

def post_to_ig(caption, image_url):
    """Post to Instagram"""
    print("📸 Instagram Basic Display API")
    print("=" * 40)
    
    # Get user info
    user = get_ig_user()
    print(f"IG User: {user}")
    
    if "error" in user:
        return user
    
    # Post image
    result = post_image(caption, image_url)
    return result

if __name__ == "__main__":
    # Test post with real image
    caption = "🧠 Testing Instagram API from EveryCompanyClaw! #AI #automation"
    # Use a test image
    image_url = "https://picsum.photos/800/800"
    
    result = post_to_ig(caption, image_url)
    print(f"\nFinal Result: {json.dumps(result, indent=2)}")
