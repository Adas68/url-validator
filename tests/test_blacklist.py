# tests/test_blacklist.py
import unittest
from utils.blacklist import check_blacklist

class TestBlacklist(unittest.TestCase):
    def test_blacklisted_url(self):
        self.assertTrue(check_blacklist("https://phishing.com "))
        self.assertTrue(check_blacklist("http://scam-site.org/login"))

    def test_safe_url(self):
        self.assertFalse(check_blacklist("https://example.com "))
        self.assertFalse(check_blacklist("https://youtube.com/watch?v=abc123"))

    def test_partial_match_does_not_trigger_false_positive(self):
        # Ensure similar domains like "goodphishing.com" aren't flagged unless exact match
        self.assertFalse(check_blacklist(" https://notphishing.com "))
        self.assertFalse(check_blacklist("https://phishing.net "))
        self.assertFalse(check_blacklist("https://badphishing.com "))

if __name__ == '__main__':
    unittest.main()