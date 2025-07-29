# test_score.py
# Unit tests for the calculate_score() function in utils/score.py
#
# PURPOSE:
# This file tests the logic used to assign a "confidence score" to a URL
# based on two factors:
#   1. Whether the URL is blacklisted (malicious)
#   2. The reputation of the final domain (good or unknown)
#
# The score helps determine how "trustworthy" a shortened URL is.
# This test ensures the scoring logic behaves exactly as intended.

# Import the built-in unittest framework — Python's standard tool for writing and running tests
import unittest

# Import the function we want to test: calculate_score()
# It is located in the utils/score.py file
# We are testing the actual production code, not a copy
from utils.score import calculate_score


class TestScore(unittest.TestCase):
    """
    TestScore is a test case class that groups all tests related to the calculate_score() function.
    
    Each method inside this class is a separate test.
    unittest will automatically discover and run every method that starts with 'test_'.
    """

    def test_blacklisted_and_unknown_reputation_returns_30(self):
        """
        TEST: Blacklisted URL with unknown reputation → Score = 30
        
        SCENARIO:
        - The URL points to a domain on the blacklist (e.g., phishing.com)
        - The domain's reputation is 'unknown' (not trusted, and WHOIS lookup failed or new domain)
        
        EXPECTED BEHAVIOR:
        - Start with base score: 100
        - Subtract 50 for being blacklisted → 50
        - Subtract 20 for unknown reputation → 30
        - Final score: 30
        
        WHY THIS MATTERS:
        This is the worst-case scenario: a known bad domain with no trust history.
        It should receive a very low score to warn users.
        """

        # CALL the function with realistic inputs:
        #   blacklisted = True → URL is malicious
        #   domain_info = {"reputation": "unknown"} → domain has no clear trust history
        score = calculate_score(
            blacklisted=True,
            domain_info={"reputation": "unknown"}
        )

        # VERIFY the result matches our expectation
        # If the score is not 30, this test will FAIL, alerting us to a bug
        self.assertEqual(score, 30)


    def test_blacklisted_url_with_good_reputation_returns_50(self):
        """
        TEST: Blacklisted URL but with good reputation → Score = 50
        
        SCENARIO:
        - The URL is blacklisted (e.g., scam-site.org)
        - BUT the domain has a good reputation (e.g., old, trusted domain like google.com)
        
        EXPECTED BEHAVIOR:
        - Start with 100
        - Subtract 50 for blacklisted → 50
        - Do NOT subtract for reputation (it's "good")
        - Final score: 50
        
        WHY THIS MATTERS:
        Even if a domain is old and trustworthy, if it's on the blacklist,
        it's still considered unsafe. But the good reputation prevents the score from dropping further.
        This prevents over-penalizing domains that might be temporarily compromised.
        """

        score = calculate_score(
            blacklisted=True,
            domain_info={"reputation": "good"}
        )

        self.assertEqual(score, 50)


    def test_safe_url_with_unknown_reputation_returns_80(self):
        """
        TEST: Safe (not blacklisted) URL with unknown reputation → Score = 80
        
        SCENARIO:
        - The URL is NOT on the blacklist
        - BUT the domain reputation is 'unknown' (e.g., newly registered or WHOIS failed)
        
        EXPECTED BEHAVIOR:
        - Start with 100
        - No penalty for blacklisting
        - Subtract 20 for unknown reputation → 80
        - Final score: 80
        
        WHY THIS MATTERS:
        Not all unknown domains are malicious, but they are suspicious.
        This score reflects caution: not dangerous, but not fully trusted either.
        """

        score = calculate_score(
            blacklisted=False,
            domain_info={"reputation": "unknown"}
        )

        self.assertEqual(score, 80)


    def test_safe_url_with_good_reputation_returns_100(self):
        """
        TEST: Safe URL with good reputation → Score = 100
        
        SCENARIO:
        - The URL is NOT blacklisted
        - The domain has a good reputation (e.g., youtube.com, google.com)
        
        EXPECTED BEHAVIOR:
        - Start with 100
        - No penalties
        - Final score: 100
        
        WHY THIS MATTERS:
        This is the ideal case — a clean, trusted URL.
        It should receive the highest possible score to indicate full confidence.
        """

        score = calculate_score(
            blacklisted=False,
            domain_info={"reputation": "good"}
        )

        self.assertEqual(score, 100)


# This block ensures that when you run this file directly:
#   python -m unittest tests/test_score.py
# the unittest framework will execute all the test methods in this class.
if __name__ == '__main__':
    unittest.main()