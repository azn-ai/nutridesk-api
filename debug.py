import requests

CLIENT_ID = input("Paste your Client ID: ").strip()
CLIENT_SECRET = input("Paste your Client Secret: ").strip()

TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
API_URL   = "https://platform.fatsecret.com/rest/server.api"

# get token
r = requests.post(TOKEN_URL, data={
    "grant_type": "client_credentials",
    "scope": "basic"
}, auth=(CLIENT_ID, CLIENT_SECRET))

print("\n--- Token response ---")
print(r.status_code, r.json())

token = r.json().get("access_token")
if not token:
    print("\nFailed to get token. Check your credentials.")
    exit()

# search
r2 = requests.get(API_URL, params={
    "method": "foods.search",
    "search_expression": "carrot",
    "format": "json",
    "max_results": 3
}, headers={"Authorization": f"Bearer {token}"})

print("\n--- Search response ---")
print(r2.status_code, r2.json())
