# utils/reputation.py
import whois
from datetime import datetime

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
        
        # Handle creation_date safely
        creation_date = info.creation_date
        
        # Case 1: creation_date is a list
        if isinstance(creation_date, list):
            # Extract valid dates and find the earliest
            valid_dates = []
            for date in creation_date:
                if hasattr(date, 'year'):
                    valid_dates.append(date)
                elif isinstance(date, str):
                    try:
                        parsed = datetime.fromisoformat(date.replace('Z', '+00:00').split('.')[0])
                        valid_dates.append(parsed)
                    except:
                        continue
            if valid_dates:
                creation_date = min(valid_dates)
            else:
                return {"reputation": "unknown"}
        
        # Case 2: creation_date is a string
        if isinstance(creation_date, str):
            try:
                creation_date = datetime.fromisoformat(creation_date.replace('Z', '+00:00').split('.')[0])
            except:
                return {"reputation": "unknown"}

        # Case 3: creation_date has year
        if hasattr(creation_date, 'year'):
            if creation_date.year < 2022:
                return {"reputation": "good"}

        return {"reputation": "unknown"}

    except Exception as e:
        # Log the error for debugging
        print(f"WHOIS lookup failed for {domain}: {e}")
        return {"reputation": "unknown"}