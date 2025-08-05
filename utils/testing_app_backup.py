from flask import Flask, request, jsonify
from utils.blacklist import check_blacklist
from utils.reputation import check_domain_reputation
from utils.score import calculate_score
from utils.datastore import load_data, save_data

import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/')
def home():
    return 'Shortened URL Validator is running!'

@app.route('/expand', methods=['POST'])
def expand_url():
    data = request.json
    short_url = data.get('url')

    if not short_url:
        return jsonify({'error': 'No URL provided'}), 400

    db = load_data()

    if short_url in db:
        return jsonify(db[short_url])  # Return cached result

    try:
        session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0"}
        response = session.get(short_url, allow_redirects=True, headers=headers)
        final_url = response.url
        redirect_chain = [r.url for r in response.history]

        # Check blacklist
        blacklist_flag = check_blacklist(final_url)

        # Domain reputation
        domain = urlparse(final_url).netloc
        domain_info = check_domain_reputation(domain)

        # Confidence Score
        score = calculate_score(blacklist_flag, domain_info)

        result = {
            "original_url": short_url,
            "final_url": final_url,
            "redirect_chain": redirect_chain,
            "blacklisted": blacklist_flag,
            "domain_reputation": domain_info,
            "confidence_score": score
        }

        db[short_url] = result
        save_data(db)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
