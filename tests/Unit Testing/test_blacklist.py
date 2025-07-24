# tests/test_blacklist.py
# This is a unit test file for the 'blacklist.py' module in the 'utils' folder.
# It tests the `check_blacklist(url)` function, which determines whether a given URL
# contains any domain from a predefined list of known malicious domains.
# The goal is to ensure that:
# - URLs with blacklisted domains (e.g., phishing.com) return True
# - Safe URLs (e.g., example.com) return False
# This helps protect users from potentially harmful links before they are expanded.

import unittest
# Import Python's built-in unittest framework.
# unittest is a standard library for writing and running tests.
# It provides tools like:
#   - TestCase: A class to group related tests
#   - assert methods (assertTrue, assertFalse): To verify expected outcomes

from utils.blacklist import check_blacklist
# Import the function we want to test: check_blacklist(url)
# This function is defined in utils/blacklist.py
# It checks if a URL contains any blacklisted domain (e.g., "phishing.com", "scam-site.org")
# It's used in the main app to flag dangerous short links during expansion.

class TestBlacklist(unittest.TestCase):
    """
    This class groups all tests related to the blacklist functionality.
    Each method inside this class is a separate test case.
    unittest will automatically discover and run every method that starts with 'test_'
    """

    def test_blacklisted_url(self):
        """
        PURPOSE: Test that a URL containing a blacklisted domain returns True.
        WHY: To ensure the app can detect and block known phishing/scam sites.
        INPUT: "https://phishing.com   " — a domain in the BLACKLISTED_DOMAINS list.
               Note: Extra whitespace is included to test robustness.
        EXPECTED OUTPUT: True (indicating the URL is blacklisted)
        """

        # Step 1: Call the function with a URL that contains a blacklisted domain
        # The input has extra spaces at the end — this tests if the function handles messy input
        result = check_blacklist("https://phishing.com   ")

        # Step 2: Assert that the result is True
        # This means the function correctly identified the URL as dangerous
        self.assertTrue(result)

        # ✅ If this passes, the function successfully flagged a malicious URL.
        # This is critical for security — we don't want users redirected to phishing sites.

    def test_safe_url(self):
        """
        PURPOSE: Test that a URL with a safe domain returns False.
        WHY: To ensure legitimate URLs are not falsely flagged as malicious (avoid false positives).
        INPUT: "https://example.com   " — a trusted, non-blacklisted domain.
               Again, extra whitespace tests input cleaning.
        EXPECTED OUTPUT: False (indicating the URL is NOT blacklisted)
        """

        # Step 1: Call the function with a safe URL
        result = check_blacklist("https://example.com   ")

        # Step 2: Assert that the result is False
        # This confirms that safe domains are allowed through
        self.assertFalse(result)

        # ✅ If this passes, the function correctly allows safe URLs.
        # Preventing false positives is important — we don’t want to block YouTube or Google.

# This block allows the test to be run directly from the command line
if __name__ == '__main__':
    """
    When this script is run directly (not imported), this condition becomes True.
    Then, unittest.main() is called, which:
    - Discovers all test methods in the TestBlacklist class
    - Runs them in order
    - Reports results (how many passed/failed)
    - Exits with status code 0 if all pass, 1 if any fail
    """
    unittest.main()