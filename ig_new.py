#!/usr/bin/env python3
import requests

token = "EAAcsIL4HlI8BQZBGqjpqZA2G4x72M1BCV23Kjgqrin4nFgg60ZBhBNuSTlXrWtgHAdVseFGAfEcRFlDBjI7LabZAUV0VA1WpxrDM4G8Cs0v1WVkGmbN0ywoijY84W5BPhHFZAOsJZADRshEoj4fCuD4QZBZCYXPDMkZCbBZCHa4hy0SLwHIi7MR88UR81Rx9WuXvZBp5PhUQMwBVekVLkkZCUGXc5NgEjpikXHpyw1OwWIp9vLWvoaukZCfacdYVkVuPFdNlQyqgq2s5kdNRdfZCnrULr5"

r = requests.get(f"https://graph.instagram.com/me?fields=id,username&access_token={token}")
print("User:", r.json())

# Try post
data = {"image_url": "https://picsum.photos/800/800", "caption": "Test", "access_token": token}
r2 = requests.post(f"https://graph.instagram.com/me/media", data=data)
print("Create:", r2.json())
