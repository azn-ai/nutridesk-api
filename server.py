from flask import Flask, request, jsonify
from flask_cors import CORS
from requests_oauthlib import OAuth1
import requests, os

app = Flask(__name__)
CORS(app)

CONSUMER_KEY    = os.environ.get("CONSUMER_KEY", "YOUR_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET", "YOUR_CONSUMER_SECRET")
API_URL = "https://platform.fatsecret.com/rest/server.api"

def auth():
    return OAuth1(CONSUMER_KEY, CONSUMER_SECRET)

def wiki_image(food_name):
    try:
        term = food_name.split(',')[0].strip().replace(' ', '_')
        r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{term}", timeout=3)
        return r.json().get('thumbnail', {}).get('source', '')
    except:
        return ''

@app.route("/search")
def search():
    query = request.args.get("q", "")
    r = requests.get(API_URL, params={
        "method": "foods.search",
        "search_expression": query,
        "format": "json",
        "max_results": 10
    }, auth=auth())
    data = r.json()
    foods = data.get('foods', {}).get('food', [])
    if isinstance(foods, dict):
        foods = [foods]

    seen = set()
    unique = []
    for f in foods:
        key = (f.get('food_name', '').lower().strip(), f.get('brand_name', '').lower().strip())
        if key not in seen:
            seen.add(key)
            f['image_url'] = wiki_image(f.get('food_name', ''))
            unique.append(f)

    if 'foods' in data:
        data['foods']['food'] = unique
    return jsonify(data)

@app.route("/food")
def food():
    food_id = request.args.get("id", "")
    r = requests.get(API_URL, params={
        "method": "food.get.v4",
        "food_id": food_id,
        "format": "json"
    }, auth=auth())
    return jsonify(r.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
