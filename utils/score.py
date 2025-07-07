def calculate_score(blacklisted, domain_info):
    score = 100

    if blacklisted:
        score -= 50

    if domain_info["reputation"] == "unknown":
        score -= 20

    return max(score, 0)
