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

    def test_get_sekret_by_id_with_no_sekret(self):
        response = self.client.get("/secret/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Secret not found"})

    def test_get_sekrets_by_space_id_with_no_sekrets(self):
        response = self.client.get("/secret/space/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Secret not found"})

    def test_get_sekrets_popular_with_no_sekrets(self):
        response = self.client.get("/secrets/popular")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])