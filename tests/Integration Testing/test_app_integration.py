# tests/integration/test_integration_full_flow.py
"""
Integration test for the full URL validation flow.
This test checks end-to-end behavior:
- Expanding a real short URL
- Checking blacklist
- Evaluating domain reputation
- Returning structured JSON

⚠️ This test makes real HTTP requests. Run only when online.
"""

import json
import unittest
import requests
from unittest.mock import patch
from utils.reputation import check_domain_reputation, normalize_domain
from utils.blacklist import check_blacklist
from production_ready_app import app

# Real short links for testing
REAL_SHORT_URLS = {
    "trusted": "https://bit.ly/4lepK9e",  # Redirects to youtube.com/watch
    "untrusted": "https://bit.ly/3V9gFqo",  # Example of unknown domain (can be changed)
}

# Mocked trusted domain for reputation mocking
MOCKED_YOUTUBE = "https://youtube.com/watch"


class TestIntegrationFullFlow(unittest.TestCase):

    def setUp(self):
        """Set up test client before each test."""
        self.client = app.test_client()

    def test_full_flow_with_trusted_short_url(self):
        """
        Test full flow with a real trusted short link.
        - Expand https://bit.ly/4lepK9e → youtube.com/watch
        - Should NOT be blacklisted
        - Should have GOOD reputation
        - Final confidence score = 100
        """
        with self.subTest("Step 1: Expand real short URL"):
            try:
                session = requests.Session()
                response = session.get(REAL_SHORT_URLS["trusted"], allow_redirects=True, timeout=10)
                final_url = response.url
                redirect_chain = [r.url for r in response.history]

                self.assertTrue(final_url.startswith("https://youtube.com/watch"))
                self.assertGreaterEqual(len(redirect_chain), 1)
            except requests.RequestException as e:
                self.fail(f"Failed to expand real short URL: {e}")

        with self.subTest("Step 2: Check not blacklisted"):
            is_blacklisted = check_blacklist(final_url)
            self.assertFalse(is_blacklisted, f"{final_url} should not be blacklisted")

        with self.subTest("Step 3: Check reputation is good"):
            domain = final_url.split("://")[1].split("/")[0]  # Extract domain
            clean_domain = normalize_domain(domain)
            result = check_domain_reputation(clean_domain)
            self.assertEqual(result["reputation"], "good", f"{clean_domain} should be trusted")

        with self.subTest("Step 4: Send to /expand endpoint and validate full response"):
            payload = {"url": REAL_SHORT_URLS["trusted"]}
            api_response = self.client.post(
                '/expand',
                data=json.dumps(payload),
                content_type='application/json'
            )
            data = json.loads(api_response.data)

            self.assertEqual(api_response.status_code, 200)
            self.assertIn("final_url", data)
            self.assertIn("redirect_chain", data)
            self.assertIn("blacklisted", data)
            self.assertIn("confidence_score", data)
            self.assertIn("reputation", data)

            self.assertFalse(data["blacklisted"])
            self.assertEqual(data["confidence_score"], 100)
            self.assertEqual(data["reputation"], "good")
            self.assertTrue("youtube.com" in data["final_url"])

    def test_full_flow_with_malicious_url(self):
        """
        Test with a known malicious or blacklisted domain.
        Since we can't use real phishing sites, we simulate one via mocking.
        """
        with patch('production_ready_app.requests.Session.get') as mock_get:
            # Simulate a blacklisted domain
            mock_response = requests.models.Response()
            mock_response.status_code = 200
            mock_response.url = "http://phishing.com/fake-login"
            mock_response.history = [type('', (), {'url': 'http://short.phish'})()]
            mock_get.return_value = mock_response

            payload = {"url": "http://short.phish"}
            response = self.client.post(
                '/expand',
                data=json.dumps(payload),
                content_type='application/json'
            )
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(data["blacklisted"])
            self.assertEqual(data["confidence_score"], 0)
            self.assertEqual(data["reputation"], "unknown")  # Not in trusted list

    def test_unknown_domain_has_unknown_reputation(self):
        """
        Test that an unknown but safe-looking domain returns 'unknown' reputation.
        """
        with patch('production_ready_app.requests.Session.get') as mock_get:
            mock_response = requests.models.Response()
            mock_response.url = "https://new-site-2025.com"
            mock_response.history = []
            mock_get.return_value = mock_response

            payload = {"url": "http://bit.ly/new-site"}
            response = self.client.post(
                '/expand',
                data=json.dumps(payload),
                content_type='application/json'
            )
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertFalse(data["blacklisted"])
            self.assertEqual(data["reputation"], "unknown")
            self.assertEqual(data["confidence_score"], 100 if not data["blacklisted"] else 0)


if __name__ == '__main__':
    unittest.main()