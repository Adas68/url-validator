# utils/production_ready_app.py
"""
Production-ready Flask app for validating shortened URLs.
- Expands short links
- Checks blacklist
- Evaluates domain reputation
- Returns structured JSON with confidence score
- Caches results to avoid repeated lookups
- Serves a simple UI at /ui
"""

from flask import Flask, request, jsonify, send_from_directory
from urllib.parse import urlparse
import requests
import json
import os
from requests.exceptions import RequestException
from utils.reputation import check_domain_reputation
from utils.blacklist import check_blacklist

app = Flask(__name__)

# Define the path to store cached URLs
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'urls.json')


def load_data():
    """Load cached URL validation results from JSON file."""
    if not os.path.exists(DATA_FILE):
        print("⚠️ Cache file not found — creating empty urls.json")
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Corrupted urls.json — resetting cache")
        return {}


def save_data(data):
    """Save updated cache to JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/')
def home():
    """Health check endpoint."""
    return 'Shortened URL Validator is running!'


@app.route('/ui')
def ui():
    """Serve the frontend UI."""
    # Go up one level from utils/ to project root, then into templates/
    templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    return send_from_directory(templates_dir, 'index.html')


@app.route('/expand', methods=['POST'])
def expand_url():
    """
    Expand a shortened URL and return:
    - Final destination
    - Redirect chain
    - Blacklist status
    - Domain reputation
    - Confidence score
    """
    data = request.get_json()
    short_url = data.get('url')

    if not short_url:
        return jsonify({
            'error': 'No URL provided. Please enter a valid short link.'
        }), 400

    # Strip whitespace (common in user input)
    short_url = short_url.strip()

    # Load cache
    db = load_data()

    # Return cached result if available
    if short_url in db:
        # Add cached flag for debugging
        result = db[short_url].copy()
        result['cached'] = True
        return jsonify(result)

    try:
        session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0 (compatible; URLValidator/1.0)"}

        # Expand shortened URL
        response = session.get(
            short_url,
            allow_redirects=True,
            headers=headers,
            timeout=10
        )

        final_url = response.url
        redirect_chain = [r.url for r in response.history]
        domain = urlparse(final_url).netloc

        # Check if domain is blacklisted
        blacklisted = check_blacklist(final_url)

        # Get domain reputation
        reputation_result = check_domain_reputation(domain)
        reputation = reputation_result["reputation"]

        # Generate confidence score
        # 100 = safe, 0 = dangerous, 50 = unknown but not blacklisted
        if blacklisted:
            score = 0
        elif reputation == "good":
            score = 100
        else:
            score = 50  # Unknown reputation, not blacklisted

        # Build result object
        result = {
            "original_url": short_url,
            "final_url": final_url,
            "redirect_chain": redirect_chain,
            "blacklisted": blacklisted,
            "reputation": reputation,
            "confidence_score": score
        }

        # Cache result
        db[short_url] = result
        save_data(db)

        return jsonify(result)

    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'The link took too long to load. It may be unsafe or broken.',
            'details': 'Request timed out'
        }), 504

    except requests.exceptions.TooManyRedirects:
        return jsonify({
            'error': 'This link redirects too many times. It may be trying to hide something dangerous.',
            'details': 'Too many redirects'
        }), 400

    except requests.exceptions.ConnectionError as e:
        return jsonify({
            'error': 'The destination website could not be reached. This link may be fake, expired, or malicious.',
            'details': str(e)
        }), 502

    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'URL expansion failed. We could not validate this link. It may be unsafe.',
            'details': str(e)
        }), 500

    except Exception as e:
        # 🔥 Fallback for ANY uncaught error (e.g., whois crash, DNS failure)
        return jsonify({
            'error': 'An unexpected error occurred while validating the link.',
            'details': f'{type(e).__name__}: {str(e)}'
        }), 500


if __name__ == '__main__':
    # Ensure data directory exists
    data_dir = os.path.dirname(DATA_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Run Flask app
    print("🚀 Starting Shortened URL Validator...")
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)