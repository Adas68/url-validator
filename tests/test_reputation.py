import unittest
from unittest.mock import patch

from utils.reputation import normalize_domain, check_domain_reputation


class TestReputation(unittest.TestCase):

    def test_normalize_domain_removes_www_and_lowercase(self):
        self.assertEqual(normalize_domain("WWW.YOUTUBE.COM"), "youtube.com")
        self.assertEqual(normalize_domain("www.github.com"), "github.com")
        self.assertEqual(normalize_domain("Google.com"), "google.com")

    def test_trusted_domains_return_good_reputation(self):
        result = check_domain_reputation("youtube.com")
        self.assertEqual(result["reputation"], "good")

        result = check_domain_reputation("github.com")
        self.assertEqual(result["reputation"], "good")

    def test_unknown_domains_return_unknown(self):
        result = check_domain_reputation("unknown-domain-xyz123.com")
        self.assertEqual(result["reputation"], "unknown")

    @patch('utils.reputation.whois.whois')
    def test_whois_lookup_returns_good_for_old_domain(self, mock_whois):
        # Simulate a WHOIS response for a domain created in 2021
        mock_whois.return_value = type('', (), {'creation_date': type('', (), {'year': 2021})})()
        result = check_domain_reputation("example.com")
        self.assertEqual(result["reputation"], "good")

    @patch('utils.reputation.whois.whois')
    def test_whois_lookup_returns_unknown_for_new_domain(self, mock_whois):
        # Simulate a WHOIS response for a domain created in 2024
        mock_whois.return_value = type('', (), {'creation_date': type('', (), {'year': 2024})})()
        result = check_domain_reputation("example.com")
        self.assertEqual(result["reputation"], "unknown")

    @patch('utils.reputation.whois.whois')
    def test_whois_lookup_returns_unknown_on_failure(self, mock_whois):
        # Simulate a WHOIS lookup failure
        mock_whois.side_effect = Exception("WHOIS lookup failed")
        result = check_domain_reputation("example.com")
        self.assertEqual(result["reputation"], "unknown")


if __name__ == '__main__':
    unittest.main()