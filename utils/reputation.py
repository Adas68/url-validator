import whois

# List of trusted domains (no www.)
trusted_domains = [
    "youtube.com",
    "google.com",
    "openai.com",
    "github.com",
    "microsoft.com",
    "apple.com",
    "linkedin.com",
    "stackoverflow.com"
]

def normalize_domain(domain):
    # Remove www. prefix if it exists
    return domain.lower().removeprefix("www.")

def check_domain_reputation(domain):
    clean_domain = normalize_domain(domain)

    # Check against trusted list
    if clean_domain in trusted_domains:
        return {"reputation": "good"}

    try:
        info = whois.whois(domain)
        if info.creation_date:
            if hasattr(info.creation_date, 'year') and info.creation_date.year < 2022:
                return {"reputation": "good"}
        return {"reputation": "unknown"}
    except:
        return {"reputation": "unknown"}
