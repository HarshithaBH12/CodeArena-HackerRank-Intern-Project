import unittest
from app import app, init_db
class SmokeTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        init_db()
    def test_health(self):
        r = self.client.get('/health')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json['status'], 'ok')
    def test_challenges(self):
        r = self.client.get('/api/challenges')
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json), 3)
    def test_home(self):
        self.assertEqual(self.client.get('/').status_code, 200)
if __name__ == '__main__': unittest.main()
