#!/usr/bin/env python3
import requests

TOKEN = "IGAAU3w4V9XB5BZAGFqLWlKT2twUW5FSk45UGZABLTRnMllkZAlRQSkNsVE5GZATF5dlNwSUNJZA0FDVlRDOVF3bE5iUWtRd2hmQUpiRFBoX05GRkU2OXBuQWFlYW5DZAHdrV1ZAiekZArSU5DdmxuTWZAuYUFxVFk0Nk5xeWY1UkktS18zcwZDZD"

# Get media
url = "https://graph.instagram.com/me?fields=id,username,media_count&access_token=" + TOKEN
r = requests.get(url)
print("User:", r.json())

# Get recent media
url2 = "https://graph.instagram.com/me/media?limit=3&access_token=" + TOKEN
r2 = requests.get(url2)
print("Recent media:", r2.json())
