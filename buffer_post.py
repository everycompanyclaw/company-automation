#!/usr/bin/env python3
"""
Buffer Instagram Auto-Post Skill
Uses Buffer GraphQL API
"""
import requests

TOKEN = "UkyLwkkW9w3-9q9MNEh0C-y71q__g2FoSYzUhaakv2K"

# Buffer GraphQL endpoint
URL = "https://api.bufferapp.com/graphql"

# Post content
POSTS = [
    "🧵 20 Python自動化腳本｜幫你慳10+粒鐘\n\n💰 $79\n\n#python #automation #hkig",
    "🤖 Build in public - AI company running 24/7\n\n$79起\n\n#buildinpublic #automation",
    "💰 Python Scripts Bundle - $79\n\n20個自動化腳本\n\n#automation #python #香港",
]

def get_profiles():
    """Get Buffer profiles"""
    query = """
    query {
        viewer {
            profiles {
                id
                service
                formatted_username
            }
        }
    }
    """
    r = requests.post(URL, json={"query": query}, headers={"Authorization": f"Bearer {TOKEN}"})
    return r.json()

def create_update(text, profile_id):
    """Create post via GraphQL"""
    query = """
    mutation CreateUpdate($input: UpdateInput!) {
        createUpdate(input: $input) {
            update {
                id
                text
            }
        }
    }
    """
    variables = {
        "input": {
            "text": text,
            "profile_ids": [profile_id]
        }
    }
    r = requests.post(URL, json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {TOKEN}"})
    return r.json()

def post_to_instagram():
    """Post to Instagram via Buffer"""
    print("📱 Posting to Buffer...")
    
    # Get profiles
    profiles = get_profiles()
    print(f"Profiles: {profiles}")
    
    # Find Instagram
    ig_profile = None
    if "data" in profiles:
        for p in profiles["data"]["viewer"]["profiles"]:
            if p.get("service") == "instagram":
                ig_profile = p
                break
    
    if not ig_profile:
        print("❌ No Instagram profile found")
        return False
    
    print(f"Found Instagram: {ig_profile}")
    
    # Post
    for post in POSTS:
        result = create_update(post, ig_profile["id"])
        print(f"Posted: {result}")
    
    return True

if __name__ == "__main__":
    post_to_instagram()
