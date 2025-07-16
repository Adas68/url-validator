import unittest
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


if __name__ == '__main__':
    unittest.main()