#!/usr/bin/env python3
"""
Instagram Graph API - Test new token
"""
import requests
import json

# New token from user
NEW_TOKEN = "EAAAAAAAAAAABQ9c5KZCrXaLF0Jugl6gmAhSGJZBx7rX1zfIdL2bwJZAfb80WMoMTX6lXFcae4CXKPhywN3ZChsQ3TecLy4J6YJd5KvOAddPTaRn2tNDJ2r0c9GUb2b5fTAvZBmiZCxWobjVAX3bTVhqurOK4gvQVPolTZAmL9ThkqiThd2EncPKFsAWO8lAAxQfmkFl9nLv3Yz9tb0RIssxGHVVahcaIssyYWGVZB8voZBr7cSwDWD94LfsEgmIvlE7yQESGgXt4q9CzkkTHRsC3RO6DZAZAbvvUgRl1RZBStBOWZBBzpLoMz1KHpU1LHPajSuI9kGuh4XPch"

IG_API = "https://graph.instagram.com"

def test_token():
    print("Testing new token...")
    
    # Get user
    url = f"{IG_API}/me?fields=id,username,media_count&access_token={NEW_TOKEN}"
    r = requests.get(url)
    user = r.json()
    print(f"User: {user}")
    
    if "id" in user:
        # Try creating media
        url2 = f"{IG_API}/{user['id']}/media"
        data = {
            "image_url": "https://picsum.photos/800/800",
            "caption": "🧠 Test from EveryCompanyClaw! #AI #automation",
            "access_token": NEW_TOKEN
        }
        r2 = requests.post(url2, data=data)
        result = r2.json()
        print(f"Create media: {result}")
        
        if "id" in result:
            # Publish
            url3 = f"{IG_API}/{user['id']}/media_publish"
            data3 = {"creation_id": result["id"], "access_token": NEW_TOKEN}
            r3 = requests.post(url3, data=data3)
            print(f"Publish: {r3.json()}")
        
    return user

test_token()
