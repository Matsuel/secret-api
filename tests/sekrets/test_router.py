import unittest
from fastapi.testclient import TestClient
from main import app

class TestSekretRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_get_sekrets_with_no_sekrets(self):
        response = self.client.get("/secrets")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "No secrets found"})