import json
import unittest
from production_ready_app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_expand_valid_short_url(self):
        payload = {"url": "http://bit.ly/example"}
        response = self.app.post('/expand', data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("final_url", data)
        self.assertIn("original_url", data)
        self.assertIn("confidence_score", data)

    def test_invalid_url_returns_error(self):
        payload = {"url": "http://invalid.short.link/xyz"}
        response = self.app.post('/expand', data=json.dumps(payload), content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)

    def test_missing_url_returns_error(self):
        payload = {}
        response = self.app.post('/expand', data=json.dumps(payload), content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "No URL provided")


if __name__ == '__main__':
    unittest.main()