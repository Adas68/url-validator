# utils/blacklist.py
#from urllib.parse import urlparse

# utils/blacklist.py
BLACKLISTED_DOMAINS = [
    "phishing.com",
    "scam-site.org",
    "malicious.site"
]

def check_blacklist(url):
    url = url.lower().strip()
    for domain in BLACKLISTED_DOMAINS:
        if domain in url:
            return True
    return False
