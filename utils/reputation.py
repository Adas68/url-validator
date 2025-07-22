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
    """
    Normalize domain by removing 'www.' prefix and converting to lowercase.
    """
    return domain.lower().removeprefix("www.")

def check_domain_reputation(domain):
    """
    Check the reputation of a domain using:
    1. Trusted domain list (fast, safe domains)
    2. WHOIS lookup (for unknown domains)
    Returns a dictionary with "reputation" key.
    """
    clean_domain = normalize_domain(domain)

    # Step 1: Check against trusted domain list
    if clean_domain in trusted_domains:
        return {"reputation": "good"}

    # Step 2: WHOIS lookup for unknown domains
    try:
        info = whois.whois(clean_domain)
        if info.creation_date:
            # Older domains (created before 2022) are considered more trustworthy
            if hasattr(info.creation_date, 'year') and info.creation_date.year < 2022:
                return {"reputation": "good"}
        return {"reputation": "unknown"}
    except Exception as e:
        # WHOIS lookup failed (e.g., invalid domain, timeout)
        return {"reputation": "unknown"}