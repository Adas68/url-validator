import unittest
from utils.blacklist import check_blacklist

class TestBlacklist(unittest.TestCase):

    def test_blacklisted_url(self):
        self.assertTrue(check_blacklist('https://phishing.com '))
        self.assertTrue(check_blacklist('http://scam-site.org/login'))

    def test_safe_url(self):
        self.assertFalse(check_blacklist('https://example.com '))
        self.assertFalse(check_blacklist('https://youtube.com/watch?v=abc123'))

if __name__ == '__main__':
    unittest.main()

