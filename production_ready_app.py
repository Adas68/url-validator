# production_ready_app.py

from flask import Flask, request, jsonify
from urllib.parse import urlparse
import requests
import json
import os
from requests.exceptions import RequestException

app = Flask(__name__)

# Define the path to store cached URLs
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'urls.json')

# Load cached URL data from JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        # Create an empty cache file if it doesn't exist
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Handle corrupted or empty JSON files
        print("⚠️ Corrupted urls.json — resetting cache")
        return {}

# Save validated URL result to cache
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Simple hardcoded blacklist (can be extended later)
BLACKLISTED_DOMAINS = [
    "phishing.com",
    "scam-site.org",
    "malicious.site",
    "stealyourdata.ru",
    "dodgy.link"
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

    # Return cached result if already validated
    if short_url in db:
        return jsonify(db[short_url])

    try:
        session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0"}

        # Expand shortened URL
        response = session.get(short_url, allow_redirects=True, headers=headers, timeout=10)

        final_url = response.url
        redirect_chain = [r.url for r in response.history]
        domain = urlparse(final_url).netloc

        # Check against known blacklisted domains
        blacklisted = check_blacklist(final_url)

        # Generate confidence score
        score = 100 if not blacklisted else 0

        # Build result object
        result = {
            "original_url": short_url,
            "final_url": final_url,
            "redirect_chain": redirect_chain,
            "blacklisted": blacklisted,
            "confidence_score": score
        }

        # Cache result
        db[short_url] = result
        save_data(db)

        return jsonify(result)

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out'}), 504

    except requests.exceptions.TooManyRedirects:
        return jsonify({'error': 'Too many redirects'}), 400

    except requests.exceptions.ConnectionError as e:
        return jsonify({
            'error': 'Failed to connect to destination',
            'details': str(e)
        }), 502

    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'URL expansion failed',
            'details': str(e)
        }), 500

    except Exception as e:
        # Fallback for unexpected errors
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    # Ensure data directory exists
    data_dir = os.path.dirname(DATA_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Run Flask app
    app.run(debug=False)