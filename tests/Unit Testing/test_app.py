'''# tests/test_app.py
import json
import unittest
from unittest.mock import patch, Mock
from production_ready_app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        """Set up test client before each test."""
        self.app = app.test_client()

    @patch('requests.Session.get')
    def test_expand_valid_short_url(self, mock_get):
        """Test expanding a valid short URL that redirects to a trusted domain."""
        mock_response = Mock()
        mock_response.url = "https://example.com "
        mock_response.history = [
            Mock(url="https://short.url "),
            Mock(url="https://intermediate.url ")
        ]
        mock_get.return_value = mock_response

        payload = {"url": "http://bit.ly/example"}
        response = self.app.post('/expand', data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("final_url", data)
        self.assertEqual(data["final_url"], "https://example.com ")
        self.assertEqual(len(data["redirect_chain"]), 2)
        self.assertFalse(data["blacklisted"])
        self.assertEqual(data["confidence_score"], 100)

    @patch('requests.Session.get')
    def test_invalid_url_returns_error(self, mock_get):
        """Test that invalid URLs return a 500 error."""
        mock_get.side_effect = Exception("Connection refused")

        payload = {"url": "http://invalid.short.link/xyz"}
        response = self.app.post('/expand', data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)

    def test_missing_url_returns_error(self):
        """Test that missing URL in payload returns a 400 error."""
        payload = {}
        response = self.app.post('/expand', data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "No URL provided")

    @patch('requests.Session.get')
    def test_timeout_error(self, mock_get):
        """Test timeout during URL expansion."""
        mock_get.side_effect = Exception("Read timed out")

        payload = {"url": "http://slow-site.com"}
        response = self.app.post('/expand', data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)

    @patch('requests.Session.get')
    def test_too_many_redirects(self, mock_get):
        """Test too many redirects scenario."""
        mock_get.side_effect = Exception("Too many redirects")

        payload = {"url": "http://redirect-loop.com"}
        response = self.app.post('/expand', data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)

    @patch('requests.Session.get')
    def test_blacklisted_domain(self, mock_get):
        """Test expanding to a blacklisted domain."""
        mock_response = Mock()
        mock_response.url = "http://phishing.com"
        mock_response.history = []
        mock_get.return_value = mock_response

        payload = {"url": "http://bit.ly/blacklisted"}
        response = self.app.post('/expand', data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["blacklisted"])
        self.assertEqual(data["confidence_score"], 0)

    @patch('requests.Session.get')
    def test_trusted_domain(self, mock_get):
        """Test expanding to a trusted domain."""
        mock_response = Mock()
        mock_response.url = "https://youtube.com/watch "
        mock_response.history = []
        mock_get.return_value = mock_response

        payload = {"url": "http://bit.ly/trusted"}
        response = self.app.post('/expand', data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data["blacklisted"])
        self.assertEqual(data["confidence_score"], 100)

if __name__ == '__main__':
    unittest.main()'''




# tests/test_app.py
import json
import unittest
from unittest.mock import patch, Mock
from production_ready_app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        """Set up a test client for the Flask app."""
        self.client = app.test_client()

    @patch('production_ready_app.requests.Session.get')
    def test_expand_valid_short_url(self, mock_get):
        # 🎯 Step 1: Simulate a successful redirect chain
        mock_response = Mock()
        mock_response.url = "https://example.com/page "
        mock_response.history = [
            Mock(url="https://bit.ly/abc123 "),
            Mock(url="https://redirect.intermediate/page ")
        ]

        # 🛠️ Step 2: Tell the mock what to return when .get() is called
        mock_get.return_value = mock_response

        # 🧪 Step 3: Send a POST request to /expand
        payload = {"url": "https://bit.ly/abc123 "}
        response = self.client.post('/expand',
                                   data=json.dumps(payload),
                                   content_type='application/json')

        # 📊 Step 4: Parse the JSON response
        data = json.loads(response.data)

        # ✅ Step 5: Assert expected behavior
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["final_url"], "https://example.com/page ")
        self.assertEqual(len(data["redirect_chain"]), 2)
        self.assertFalse(data["blacklisted"])
        self.assertEqual(data["confidence_score"], 100)

    @patch('production_ready_app.requests.Session.get')
    def test_invalid_url_returns_error(self, mock_get):
        # 🚨 Simulate a connection failure
        mock_get.side_effect = Exception("Failed to connect")

        # 🧪 Send invalid URL
        payload = {"url": "http://this-does-not-exist.xyz"}
        response = self.client.post('/expand',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        data = json.loads(response.data)

        # ✅ Should return 500 (internal error), not 502!
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)

    def test_missing_url_returns_error(self):
        # 🧪 Send empty payload
        payload = {}
        response = self.client.post('/expand',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        data = json.loads(response.data)

        # ✅ Should return 400
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "No URL provided")