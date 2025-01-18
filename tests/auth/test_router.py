import unittest
from fastapi.testclient import TestClient
from main import app

class TestAuthRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_get_auth_with_no_curent_user(self):
        response = self.client.get("/users/me")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})