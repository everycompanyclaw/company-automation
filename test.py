#!/usr/bin/env python3
import requests

token = "EAAcsIL4HlI8BQwCZB3faUDKzZCnP7TA785ZB9MeLojbgTZCCjScvrhRyBDfyDYjwWTe2AkeuuqSaP9ZAomQOm8MeAse9EbdcgCTZAJz6OVBYpQ1EfT44iS4utLDp7pxt4WdAafYKKWaTZBzyx1hsmUW8UjmXPZA6o5TiUsZA8e8zsrGLZBwobxt26N6fOeYL9Ba9kbUBRd4wE1pHHKG444wYWaw6MWNrrVQRUdBftVN6AXRuZBXg4ilxXpHsBlRKdijejurnx0bs4pSwSrgo8knEvxjvZCgfwQZDZD"

# Test token
r = requests.get(f"https://graph.facebook.com/v18.0/me?fields=id,name&access_token={token}")
print("User:", r.json())

# Get pages
r2 = requests.get(f"https://graph.facebook.com/v18.0/me/accounts?access_token={token}")
print("Pages:", r2.json())
