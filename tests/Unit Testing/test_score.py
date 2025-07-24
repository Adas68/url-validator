import unittest
from utils.score import calculate_score

class TestScore(unittest.TestCase):

    def test_blacklisted_url_returns_50(self):
        result = calculate_score(blacklisted=True, domain_info={"reputation": "good"})
        self.assertEqual(result, 50)

    def test_unknown_domain_returns_80(self):
        result = calculate_score(blacklisted=False, domain_info={"reputation": "unknown"})
        self.assertEqual(result, 80)

    def test_blacklisted_and_unknown_returns_30(self):
        result = calculate_score(blacklisted=True, domain_info={"reputation": "unknown"})
        self.assertEqual(result, 30)

    def test_good_reputation_returns_100(self):
        result = calculate_score(blacklisted=False, domain_info={"reputation": "good"})
        self.assertEqual(result, 100)


if __name__ == '__main__':
    unittest.main()