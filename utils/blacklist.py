from urllib.parse import urlparse

def check_blacklist(url):
    blacklisted_domains = [
        "phishing.com",
        "malware.com",
        "scam-site.net"
    ]
    domain = urlparse(url).netloc.lower()
    return any(bad in domain for bad in blacklisted_domains)
