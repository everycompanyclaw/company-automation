#!/usr/bin/env python3
import requests

token = "EAAcsIL4HlI8BQwCZB3faUDKzZCnP7TA785ZB9MeLojbgTZCCjScvrhRyBDfyDYjwWTe2AkeuuqSaP9ZAomQOm8MeAse9EbdcgCTZAJz6OVBYpQ1EfT44iS4utLDp7pxt4WdAafYKKWaTZBzyx1hsmUW8UjmXPZA6o5TiUsZA8e8zsrGLZBwobxt26N6fOeYL9Ba9kbUBRd4wE1pHHKG444wYWaw6MWNrrVQRUdBftVN6AXRuZBXg4ilxXpHsBlRKdijejurnx0bs4pSwSrgo8knEvxjvZCgfwQZDZD"

# Get IG business account
r = requests.get(f"https://graph.facebook.com/v18.0/122096802212948996?fields=instagram_business_account&access_token={token}")
print("IG Account:", r.json())

# Try to get media
if "instagram_business_account" in r.json():
    ig_id = r.json()["instagram_business_account"]["id"]
    r2 = requests.get(f"https://graph.facebook.com/v18.0/{ig_id}/media?access_token={token}")
    print("Media:", r2.json())
