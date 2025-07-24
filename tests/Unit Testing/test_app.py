# tests/test_app.py
# This is a unit test file for the Flask app in 'production_ready_app.py'.
# It tests the '/expand' endpoint that expands short URLs and checks their reputation.
# We use unittest.mock to simulate external HTTP requests so our tests are:
# - Fast (no real network calls)
# - Reliable (no dependency on Bitly, YouTube, etc.)
# - Repeatable (same input → same output every time)

import json
import unittest
# Import the unittest framework — Python's built-in library for writing and running tests.

from unittest.mock import patch, Mock
# Import tools for mocking:
# - 'patch': Temporarily replaces a function (like requests.get) with a fake version.
# - 'Mock': A fake object that acts like the real thing but doesn't do real work.

from production_ready_app import app
# Import the Flask app instance so we can test its routes.
# This is the app that handles POST /expand requests.

class TestApp(unittest.TestCase):
    """
    This class contains multiple test methods to verify the behavior of the Flask app.
    Each test simulates a different scenario: valid URL, invalid URL, missing URL, etc.
    """

    def setUp(self):
        """
        PURPOSE: Set up the test environment before each test method runs.
        WHY: Ensures a clean state for every test.
        HOW: Creates a test client that can make requests to the Flask app without starting a server.
        """
        # Create a test client for the Flask app
        # This client lets us send fake HTTP requests (like POST) to endpoints like '/expand'
        self.client = app.test_client()

    @patch('production_ready_app.requests.Session.get')
    def test_expand_valid_short_url(self, mock_get):
        """
        PURPOSE: Test that a valid short URL is expanded correctly and returns expected JSON.
        WHY: To ensure the app works when a user submits a real short link (e.g., bit.ly/xyz).
        HOW: We mock the actual HTTP request to avoid real network calls.
        """

        # Step 1: Create a mock response object to simulate what requests.get() would return
        mock_response = Mock()
        # This is a fake version of the response object from requests.get()

        # Step 2: Simulate the final destination URL after all redirects
        mock_response.url = "https://example.com/page"
        # If someone visits the short link, they eventually land here.

        # Step 3: Simulate the redirect chain (list of intermediate URLs)
        mock_response.history = [
            Mock(url="https://bit.ly/abc123"),           # First redirect
            Mock(url="https://redirect.intermediate/page")  # Second redirect
        ]
        # These are the URLs the browser passes through before reaching the final page.

        # Step 4: Tell the mock what to return when .get() is called
        mock_get.return_value = mock_response
        # Now, whenever the app calls requests.Session.get(short_url), it gets our fake response.

        # Step 5: Prepare the JSON payload (what the user sends)
        payload = {"url": "https://bit.ly/abc123"}

        # Step 6: Send a POST request to the /expand endpoint
        response = self.client.post(
            '/expand',                          # Endpoint to test
            data=json.dumps(payload),           # Convert dict to JSON string
            content_type='application/json'     # Tell Flask it's JSON
        )

        # Step 7: Parse the JSON response from the app
        data = json.loads(response.data)

        # Step 8: Assert expected behavior — check if the app responded correctly
        self.assertEqual(response.status_code, 200)  # Should return 200 OK
        self.assertEqual(data["final_url"], "https://example.com/page")  # Final URL matches
        self.assertEqual(len(data["redirect_chain"]), 2)  # Two redirects occurred
        self.assertFalse(data["blacklisted"])  # Not in blacklist
        self.assertEqual(data["confidence_score"], 100)  # Trusted domain → high confidence

        # ✅ This confirms the app correctly expands short links and builds the result.

    @patch('production_ready_app.requests.Session.get')
    def test_invalid_url_returns_error(self, mock_get):
        """
        PURPOSE: Test that an invalid short URL returns a 500 Internal Server Error.
        WHY: To ensure the app fails gracefully when a network error occurs.
        HOW: We simulate a connection failure using side_effect.
        """

        # Step 1: Make the mocked .get() call raise an exception
        mock_get.side_effect = Exception("Failed to connect to destination")
        # This simulates scenarios like:
        # - The domain doesn't exist
        # - The server is down
        # - DNS lookup fails

        # Step 2: Prepare payload with a bad URL
        payload = {"url": "http://this-does-not-exist.xyz"}

        # Step 3: Send POST request
        response = self.client.post(
            '/expand',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Step 4: Parse response
        data = json.loads(response.data)

        # Step 5: Assert expected behavior
        self.assertEqual(response.status_code, 500)  # Internal Server Error
        self.assertIn("error", data)  # Response includes an error message

        # ✅ This confirms the app handles network failures safely.

    def test_missing_url_returns_error(self):
        """
        PURPOSE: Test that submitting no URL returns a 400 Bad Request.
        WHY: To validate input validation logic.
        HOW: Send an empty JSON payload.
        """

        # Step 1: Send POST request with no 'url' field
        payload = {}
        response = self.client.post(
            '/expand',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Step 2: Parse response
        data = json.loads(response.data)

        # Step 3: Assert expected behavior
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertEqual(data["error"], "No URL provided")  # Correct error message

        # ✅ This confirms the app validates input before processing.

# This block allows the test to be run directly from the command line
if __name__ == '__main__':
    # unittest.main() discovers and runs all test methods in this class
    unittest.main()