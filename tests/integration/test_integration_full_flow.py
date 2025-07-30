# tests/integration/test_integration_full_flow.py
import json
import unittest
from unittest.mock import patch, Mock
from production_ready_app import app

class TestIntegrationFullFlow(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_trusted_short_url_expands_and_returns_full_data(self):
        """Test full flow with a real trusted short URL."""
        payload = {"url": "https://bit.ly/4lepK9e"}

        response = self.client.post(
            '/expand',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.data)

        # Assert expected behavior
        self.assertEqual(response.status_code, 200)
        self.assertIn("final_url", data)
        self.assertTrue("youtube.com" in data["final_url"])
        self.assertFalse(data["blacklisted"])
        self.assertEqual(data["confidence_score"], 100)
        self.assertGreaterEqual(len(data["redirect_chain"]), 1)

    @patch('production_ready_app.requests.Session.get')
    def test_blacklisted_url_returns_zero_score(self, mock_get):
        mock_response = Mock()
        mock_response.url = "http://phishing.com/fake-login"
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