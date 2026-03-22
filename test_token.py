#!/usr/bin/env python3
import requests
import json

token = "EAAcsIL4HlI8BQZBGqjpqZA2G4x72M1BCV23Kjgqrin4nFgg60ZBhBNuSTlXrWtgHAdVseFGAfEcRFlDBjI7LabZAUV0VA1WpxrDM4G8Cs0v1WVkGmbN0ywoijY84W5BPhHFZAOsJZADRshEoj4fCuD4QZBZCYXPDMkZCbBZCHa4hy0SLwHIi7MR88UR81Rx9WuXvZBp5PhUQMwBVekVLkkZCUGXc5NgEjpikXHpyw1OwWIp9vLWvoaukZCfacdYVkVuPFdNlQyqgq2s5kdNRdfZCnrULr5"

# Test with Facebook Graph API first
r = requests.get(f"https://graph.facebook.com/v18.0/me?fields=id,name&access_token={token}")
print("FB User:", r.json())

# Get accounts
r2 = requests.get(f"https://graph.facebook.com/v18.0/me/accounts?access_token={token}")
print("Accounts:", r2.json())
