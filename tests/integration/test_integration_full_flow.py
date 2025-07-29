# tests/integration/test_integration_full_flow.py
"""
Integration test for the full URL validation flow.
Tests how all components work together:
- Flask app (/expand endpoint)
- URL expansion via requests
- Blacklist checking
- Domain reputation logic
- Caching
"""

import json
import unittest
import requests
from unittest.mock import patch, Mock

# Import your Flask app
from production_ready_app import app

# Real short link that safely redirects to YouTube
TRUSTED_SHORT_URL = "https://bit.ly/4lepK9e"  # → youtube.com/watch
INVALID_SHORT_URL = "http://this-does-not-exist.xyz"
BLACKLISTED_URL = "http://phishing.com/fake-login"


class TestIntegrationFullFlow(unittest.TestCase):

    def setUp(self):
        """Set up test client before each test."""
        self.client = app.test_client()

    def test_trusted_short_url_expands_correctly(self):
        """Test that a real trusted short URL expands and returns correct JSON."""
        payload = {"url": TRUSTED_SHORT_URL}

        try:
            response = self.client.post(
                '/expand',
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)

            data = json.loads(response.data)

            # Verify expected fields
            self.assertIn("final_url", data)
            self.assertIn("redirect_chain", data)
            self.assertIn("blacklisted", data)
            self.assertIn("confidence_score", data)
            self.assertIn("reputation", data)

            # Should point to YouTube
            self.assertTrue("youtube.com" in data["final_url"])
            self.assertFalse(data["blacklisted"])
            self.assertEqual(data["reputation"], "good")
            self.assertEqual(data["confidence_score"], 100)

        except requests.exceptions.RequestException as e:
            self.fail(f"Network error during test: {e}")

    @patch('requests.Session.get')
    def test_blacklisted_url_returns_zero_confidence(self, mock_get):
        """Test that a blacklisted domain returns blacklisted=True and score=0."""
        # Simulate response from a blacklisted domain
        mock_response = Mock()
        mock_response.url = "http://phishing.com/fake-login"
        mock_response.history = [Mock(url="http://short.phish")]
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

    @patch('requests.Session.get')
    def test_new_domain_has_unknown_reputation(self, mock_get):
        """Test that a new, unknown domain returns reputation=unknown."""
        mock_response = Mock()
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
        self.assertEqual(data["confidence_score"], 100)  # Only blacklisting affects score

    def test_missing_url_returns_400(self):
        """Test that missing URL in payload returns 400 Bad Request."""
        payload = {}
        response = self.client.post(
            '/expand',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "No URL provided")


if __name__ == '__main__':
    unittest.main()