#!/usr/bin/env python3
"""
Instagram Auto-Post - Using Jellyfish-generated images
"""
import requests
import time
import os

TOKEN = "IGAAU3w4V9XB5BZAGFqLWlKT2twUW5FSk45UGZABLTRnMllkZAlRQSkNsVE5GZATF5dlNwSUNJZA0FDVlRDOVF3bE5iUWtRd2hmQUpiRFBoX05GRkU2OXBuQWFlYW5DZAHdrV1ZAiekZArSU5DdmxuTWZAuYUFxVFk0Nk5xeWY1UkktS18zcwZDZD"

def create_media_container(image_url, caption):
    """Create media container"""
    url = "https://graph.instagram.com/me/media"
    data = {
        "image_url": image_url,
        "caption": caption,
        "access_token": TOKEN
    }
    r = requests.post(url, data=data)
    return r.json()

def publish_media(container_id):
    """Publish media from container"""
    url = "https://graph.instagram.com/me/media_publish"
    data = {
        "creation_id": container_id,
        "access_token": TOKEN
    }
    r = requests.post(url, data=data)
    return r.json()

def post_to_instagram(image_url, caption):
    """Full posting flow"""
    # Step 1: Create container
    print("Creating media container...")
    result = create_media_container(image_url, caption)
    print(f"Container: {result}")
    
    if "id" in result:
        container_id = result["id"]
        print(f"Container ID: {container_id}")
        
        # Step 2: Publish (wait a bit)
        print("Publishing...")
        time.sleep(2)
        publish_result = publish_media(container_id)
        print(f"Published: {publish_result}")
        return publish_result
    
    return result

if __name__ == "__main__":
    # Test with the Jellyfish service
    print("🖼️ Instagram Auto-Post Test")
    print("=" * 40)
    
    # You can generate an image with Jellyfish at localhost:7788
    # Then use the local file path
    image_path = input("Enter image path (or press Enter to use default): ").strip()
    
    if not image_path:
        # Use a sample Unsplash image that Instagram might accept
        image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/800px-Camponotus_flavomarginatus_ant.jpg"
    else:
        image_url = image_path
    
    caption = "Test post from EveryCompanyClaw! 🤖 #AI #automation"
    
    result = post_to_instagram(image_url, caption)
    print("\nFinal Result:", result)
