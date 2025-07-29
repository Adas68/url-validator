# tests/test_reputation.py
# This is a unit test file for the 'reputation.py' module.
# It verifies that the domain reputation logic works correctly.
# We are using Python's built-in unittest framework and unittest.mock to simulate external behavior.

import unittest
# Import the unittest framework — this is Python's standard library for writing and running tests.

from unittest.mock import patch
# Import 'patch' from unittest.mock.
# 'patch' is a decorator/context manager that temporarily replaces an object (like a function or module)
# with a mock version during the test. This allows us to simulate external services (like WHOIS) without
# making real network calls.

from utils.reputation import normalize_domain, check_domain_reputation
# Import the two functions we want to test:
# - normalize_domain(): removes 'www.' and converts to lowercase
# - check_domain_reputation(): evaluates if a domain is "good" or "unknown"


class TestReputation(unittest.TestCase):
    """
    This test class contains multiple test methods to verify the behavior of the reputation module.
    Each test checks a specific scenario to ensure the code behaves as expected.
    """

    def test_normalize_domain_removes_www_and_lowercase(self):
        """
        PURPOSE: Test that the normalize_domain() function correctly:
                 - Removes the 'www.' prefix (if present)
                 - Converts the domain to lowercase
        WHY: This ensures consistent comparison when checking trusted domains.
        """

        # Test case 1: Mixed case with 'www.' prefix
        # Input: "WWW.YOUTUBE.COM" → Expected: "youtube.com"
        self.assertEqual(normalize_domain("WWW.YOUTUBE.COM"), "youtube.com")

        # Test case 2: Lowercase with 'www.' prefix
        # Input: "www.github.com" → Expected: "github.com"
        self.assertEqual(normalize_domain("www.github.com"), "github.com")

        # Test case 3: Mixed case without 'www.', but needs lowercase
        # Input: "Google.com" → Expected: "google.com"
        self.assertEqual(normalize_domain("Google.com"), "google.com")

        # ✅ If all assertions pass, the function correctly normalizes domains for comparison.


    def test_trusted_domains_return_good_reputation(self):
        """
        PURPOSE: Test that domains in the 'trusted_domains' list return {"reputation": "good"}.
        WHY: We have a hardcoded list of known safe domains (e.g., google.com). This test ensures
             they are immediately recognized as trustworthy without needing a WHOIS lookup.
        """

        # Test case 1: Check a domain in the trusted list
        result = check_domain_reputation("youtube.com")
        # Expected: {"reputation": "good"}
        self.assertEqual(result["reputation"], "good")

        # Test case 2: Check another trusted domain
        result = check_domain_reputation("github.com")
        # Expected: {"reputation": "good"}
        self.assertEqual(result["reputation"], "good")

        # ✅ If both pass, the trusted domain check is working correctly.
        # This avoids unnecessary WHOIS lookups for known good domains.


    def test_unknown_domains_return_unknown(self):
        """
        PURPOSE: Test that a domain NOT in the trusted list returns {"reputation": "unknown"}.
        WHY: Ensures fallback behavior for domains we don't recognize.
        NOTE: This test does NOT trigger a real WHOIS lookup — it just checks the fast path.
        """

        # Test case: Use a fake, non-existent domain
        result = check_domain_reputation("unknown-domain-xyz123.com")
        # Expected: {"reputation": "unknown"}
        self.assertEqual(result["reputation"], "unknown")

        # ✅ This confirms that unknown domains are not falsely marked as "good".


    @patch('utils.reputation.whois.whois')
    def test_whois_lookup_returns_good_for_old_domain(self, mock_whois):
        """
        PURPOSE: Test that a WHOIS lookup for an OLD domain (created before 2022) returns "good".
        WHY: Older domains are considered more trustworthy (less likely to be phishing/scam).
        HOW: We use @patch to replace the real 'whois.whois()' function with a mock.
             This mock returns a simulated WHOIS response with a creation date of 2021.
        """

        # Step 1: Simulate a WHOIS response object
        # We use Python's 'type()' to dynamically create an object that mimics the real WHOIS result.
        # Structure:
        #   whois.whois(domain) → returns an object with a 'creation_date' attribute
        #   creation_date.year = 2021
        mock_whois.return_value = type(
            '',  # Anonymous class name
            (),  # No base classes
            {   # Attributes of the object
                'creation_date': type('', (), {'year': 2021})()  # creation_date has .year = 2021
            }
        )()

        # Step 2: Call the function under test
        result = check_domain_reputation("example.com")

        # Step 3: Assert the expected behavior
        # Since 2021 < 2022, the domain should be considered "good"
        self.assertEqual(result["reputation"], "good")

        # ✅ This confirms that old domains are correctly identified as trustworthy.
        # The mock prevents a real WHOIS call — fast, reliable, and safe.


    @patch('utils.reputation.whois.whois')
    def test_whois_lookup_returns_unknown_for_new_domain(self, mock_whois):
        """
        PURPOSE: Test that a WHOIS lookup for a NEW domain (created in 2024) returns "unknown".
        WHY: New domains are more likely to be malicious (e.g., phishing sites).
        HOW: Again, we mock the WHOIS response, but this time with creation_date.year = 2024.
        """

        # Step 1: Simulate a WHOIS response with a recent creation date
        mock_whois.return_value = type(
            '',
            (),
            {
                'creation_date': type('', (), {'year': 2024})()
            }
        )()

        # Step 2: Call the function
        result = check_domain_reputation("example.com")

        # Step 3: Assert the expected behavior
        # Since 2024 >= 2022, it should return "unknown"
        self.assertEqual(result["reputation"], "unknown")

        # ✅ This confirms that new domains are not trusted by default.
        # The logic is working as intended.


    @patch('utils.reputation.whois.whois')
    def test_whois_lookup_returns_unknown_on_failure(self, mock_whois):
        """
        PURPOSE: Test that if the WHOIS lookup FAILS (e.g., network error, invalid domain),
                 the function safely returns {"reputation": "unknown"}.
        WHY: We don't want our app to crash if WHOIS is down or slow.
             This ensures graceful degradation.
        HOW: We use 'side_effect' to make the mock raise an exception when called.
        """

        # Step 1: Make the mock raise an exception when whois.whois() is called
        mock_whois.side_effect = Exception("WHOIS lookup failed: Connection timeout or invalid domain")

        # Step 2: Call the function
        result = check_domain_reputation("example.com")

        # Step 3: Assert the expected behavior
        # Even though WHOIS failed, the function should return "unknown", not crash
        self.assertEqual(result["reputation"], "unknown")

        # ✅ This confirms that the try-except block in reputation.py works correctly.
        # The app remains stable even when external services fail.

# This block allows the test to be run directly from the command line
if __name__ == '__main__':
    # unittest.main() discovers and runs all test methods in this class
    unittest.main()