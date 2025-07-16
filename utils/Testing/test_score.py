import unittest
from utils.score import calculate_score

class TestScore(unittest.TestCase):

    def test_blacklisted_url_returns_zero(self):
        score = calculate_score(blacklisted=True, reputation={"reputation": "unknown"})
        self.assertEqual(score, 0)

    def test_known_good_domain_returns_hundred(self):
        score = calculate_score(blacklisted=False, reputation={"reputation": "good"})
        self.assertEqual(score, 100)

    def test_unknown_domain_returns_fifty(self):
        score = calculate_score(blacklisted=False, reputation={"reputation": "unknown"})
        self.assertEqual(score, 50)


if __name__ == '__main__':
    unittest.main()