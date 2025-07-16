# 🔍 Shortened URL Validator

A Flask-based backend service that validates shortened URLs by expanding them, checking domain reputation, and returning safety info without visiting the link.

## 📌 Project Description

The **Shortened URL Validator** is a lightweight Python tool designed to help users assess the **safety of shortened URLs** (like those from Bitly or TinyURL) **without visiting them directly**.

It:
- Expands shortened URLs to their final destination
- Tracks redirect chains
- Checks against a list of known malicious domains
- Evaluates domain trustworthiness using WHOIS lookup
- Returns a confidence score (0–100)
- Caches validated results for faster future lookups

This helps users determine if a short link leads to a safe or suspicious website.

## 🧰 Features

✅ Accepts POST requests with short URL  
✅ Expands to full destination URL  
✅ Tracks all redirect steps  
✅ Checks against phishing/malware domains  
✅ Evaluates domain trustworthiness  
✅ Returns structured JSON output  
✅ Caches validated URLs for performance  
✅ Handles errors gracefully (timeout, DNS issues)

## 📁 Folder Structure

Your project should follow this structure:

url-validator/
│
├── production_ready_app.py # Main Flask app
├── utils/
│ ├── blacklist.py # Blacklist check
│ ├── reputation.py # Domain reputation logic
│ └── score.py # Confidence scoring system
│
├── data/
│ └── urls.json # Stores cached results
│
├── tests/
│ ├── test_blacklist.py # Unit test for blacklist
│ ├── test_reputation.py # Unit test for reputation checks
│ └── test_app.py # Integration test for full endpoint
│
├── .gitignore # Files to ignore in Git
├── requirements.txt # Python dependencies
└── README.md # This file


## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Adas68/url-validator.git 
cd url-validator


2. Create Virtual Environment

python -m venv venv
.\venv\Scripts\activate


3. Install Dependencies

pip install -r requirements.txt

"Requirements include: "
Flask==2.3.3
requests==2.31.0
python-whois==0.9.5


4. Ensure Datastore Exists

mkdir data
echo {} > data\urls.json

5. Run the App

set FLASK_APP=production_ready_app.py
flask run

🧪 How to Test the API
You can use PowerShell, curl, or tools like Postman to test.

Example Request (PowerShell):

$url = "http://localhost:5000/expand"
$headers = @{ "Content-Type" = "application/json" }
$body = '{"url": "http://bit.ly/example"}'

$response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -Body $body
$response | ConvertTo-Json -Depth 5


profile
Qwen3-235B-A22B
Here is a clean, professional, and ready-to-use README.md file for your GitHub repository.

You can copy and paste this directly into a new file called README.md in your project root folder.


# 🔍 Shortened URL Validator

A Flask-based backend service that validates shortened URLs by expanding them, checking domain reputation, and returning safety info without visiting the link.

## 📌 Project Description

The **Shortened URL Validator** is a lightweight Python tool designed to help users assess the **safety of shortened URLs** (like those from Bitly or TinyURL) **without visiting them directly**.

It:
- Expands shortened URLs to their final destination
- Tracks redirect chains
- Checks against a list of known malicious domains
- Evaluates domain trustworthiness using WHOIS lookup
- Returns a confidence score (0–100)
- Caches validated results for faster future lookups

This helps users determine if a short link leads to a safe or suspicious website.

## 🧰 Features

✅ Accepts POST requests with short URL  
✅ Expands to full destination URL  
✅ Tracks all redirect steps  
✅ Checks against phishing/malware domains  
✅ Evaluates domain trustworthiness  
✅ Returns structured JSON output  
✅ Caches validated URLs for performance  
✅ Handles errors gracefully (timeout, DNS issues)

## 📁 Folder Structure

Your project should follow this structure:

url-validator/
│
├── production_ready_app.py # Main Flask app
├── utils/
│ ├── blacklist.py # Blacklist check
│ ├── reputation.py # Domain reputation logic
│ └── score.py # Confidence scoring system
│
├── data/
│ └── urls.json # Stores cached results
│
├── tests/
│ ├── test_blacklist.py # Unit test for blacklist
│ ├── test_reputation.py # Unit test for reputation checks
│ └── test_app.py # Integration test for full endpoint
│
├── .gitignore # Files to ignore in Git
├── requirements.txt # Python dependencies
└── README.md # This file



## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Adas68/url-validator.git 
cd url-validator
2. Create Virtual Environment
powershell


1
2
python -m venv venv
.\venv\Scripts\activate
3. Install Dependencies
powershell


1
pip install -r requirements.txt
Requirements include: 



1
2
3
Flask==2.3.3
requests==2.31.0
python-whois==0.9.5
4. Ensure Datastore Exists
powershell


1
2
mkdir data
echo {} > data\urls.json
5. Run the App
powershell



set FLASK_APP=production_ready_app.py
flask run
🧪 How to Test the API
You can use PowerShell, curl, or tools like Postman to test.

Example Request (PowerShell):


'''$url = "http://localhost:5000/expand"
$headers = @{ "Content-Type" = "application/json" }
$body = '{"url": "http://bit.ly/example"}'

$response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -Body $body
$response | ConvertTo-Json -Depth 5'''

///
Sample Response:

{
    "original_url": "http://bit.ly/example",
    "final_url": "https://example.com ",
    "redirect_chain": ["http://bit.ly/example", "https://example.com "],
    "blacklisted": false,
    "domain_reputation": {"reputation": "good"},
    "confidence_score": 100
}

🔒 Security & Trust Evaluation
Blacklist Check
Compares final URL against known malicious domains such as:

phishing.com
scam-site.org
malicious.site
Defined in utils/blacklist.py

Domain Reputation
Checks:

If domain is in trusted list (e.g., youtube.com, github.com)
Uses WHOIS to evaluate domain age
Returns "good" or "unknown"
Defined in utils/reputation.py

Confidence Score
Blacklisted
0
Trusted domain
100
Unknown domain
50

Can be extracted to utils/score.py later

💾 Caching System
Results are saved in data/urls.json
Prevents re-checking the same URL
Improves performance
Safe to modify or clear manually
🛡️ Error Handling
Handles these common cases:

Empty or missing URL
Malformed JSON input
Timeout during expansion
Too many redirects
Connection failure (DNS / unreachable)
General exceptions
Returns clean JSON error messages instead of crashing.

📦 Future Enhancements (Phase 2)
Planned improvements:

Add user authentication (API keys or OAuth)
Implement rate limiting per user/IP
Deploy online using Render or Heroku
Build HTML frontend for easy usage
Integrate Google Safe Browsing or VirusTotal API
Create browser extension version
👨‍💻 Collaborator
User: vanuverma
Role: Reviewer / Contributor
GitHub Access: Add as collaborator to the repo

📝 License
TBD – You may add MIT or another license later.