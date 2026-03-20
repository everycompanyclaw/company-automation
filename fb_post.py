#!/usr/bin/env python3
"""
Facebook Graph API Auto-Post
"""
import requests
import os

# Facebook Graph API endpoint
FB_API = "https://graph.facebook.com/v18.0"

# Need these credentials:
# 1. PAGE_ID - Your Facebook Page ID
# 2. ACCESS_TOKEN - Facebook Page Access Token

PAGE_ID = os.environ.get("FB_PAGE_ID", "")
ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN", "")

def post_to_facebook(message, page_id=None, access_token=None):
    """Post to Facebook Page via Graph API"""
    
    page_id = page_id or PAGE_ID
    access_token = access_token or ACCESS_TOKEN
    
    if not page_id or not access_token:
        print("❌ Need Facebook credentials!")
        print("\nTo get access:")
        print("1. Go to developers.facebook.com")
        print("2. Create App")
        print("3. Add Marketing API")
        print("4. Get Page Access Token")
        print("\nSet environment:")
        print("  FB_PAGE_ID=your_page_id")
        print("  FB_ACCESS_TOKEN=your_token")
        return {"error": "missing_credentials"}
    
    url = f"{FB_API}/{page_id}/feed"
    
    data = {
        "message": message,
        "access_token": access_token
    }
    
    try:
        r = requests.post(url, data=data, timeout=10)
        result = r.json()
        
        if "id" in result:
            print(f"✅ Posted! Post ID: {result['id']}")
            return {"success": True, "post_id": result['id']}
        else:
            print(f"❌ Error: {result}")
            return {"error": result}
    except Exception as e:
        print(f"❌ Exception: {e}")
        return {"error": str(e)}

def post_with_image(message, image_url, page_id=None, access_token=None):
    """Post image to Facebook"""
    
    page_id = page_id or PAGE_ID
    access_token = access_token or ACCESS_TOKEN
    
    if not page_id or not access_token:
        return {"error": "missing_credentials"}
    
    url = f"{FB_API}/{page_id}/photos"
    
    data = {
        "message": message,
        "url": image_url,
        "access_token": access_token
    }
    
    try:
        r = requests.post(url, data=data, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test post
    test_message = "🧠 AI Company testing Facebook API posting!\n\n#automation #AI #python"
    
    result = post_to_facebook(test_message)
    print(result)
