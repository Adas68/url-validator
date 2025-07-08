import unittest
import json
from app import check_blacklist, load_data

class TestURLValidator(unittest.TestCase):

    def test_blacklist_check(self):
        self.assertTrue(check_blacklist("https://phishing.com "))
        self.assertFalse(check_blacklist("https://safe.com "))

    def test_load_data(self):
        db = load_data()
        self.assertIsInstance(db, dict)

if __name__ == '__main__':
    unittest.main()