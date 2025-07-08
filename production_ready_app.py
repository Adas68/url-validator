# app.py

from flask import Flask, request, jsonify
from urllib.parse import urlparse
import requests
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'urls.json')

# Load cached URLs
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save URL result to cache
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Simple hardcoded blacklist
BLACKLISTED_DOMAINS = [
    "phishing.com", "scam-site.org", "malicious.site"
]

def check_blacklist(url):
    for domain in BLACKLISTED_DOMAINS:
        if domain in url:
            return True
    return False

@app.route('/')
def home():
    return 'Shortened URL Validator is running!'

@app.route('/expand', methods=['POST'])
def expand_url():
    data = request.get_json()
    short_url = data.get('url')

    if not short_url:
        return jsonify({'error': 'No URL provided'}), 400

    db = load_data()

    if short_url in db:
        return jsonify(db[short_url])

    try:
        session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0"}
        response = session.get(short_url, allow_redirects=True, headers=headers, timeout=10)

        final_url = response.url
        redirect_chain = [r.url for r in response.history]
        domain = urlparse(final_url).netloc

        blacklisted = check_blacklist(final_url)
        score = 100 if not blacklisted else 0

        result = {
            "original_url": short_url,
            "final_url": final_url,
            "redirect_chain": redirect_chain,
            "blacklisted": blacklisted,
            "confidence_score": score
        }

        db[short_url] = result
        save_data(db)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)