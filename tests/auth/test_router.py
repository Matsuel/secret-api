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

    def test_get_test_token_with_no_auth(self):
        response = self.client.get("/test-token")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    def test_post_login_with_no_user(self):
        response = self.client.post("/login", data={"username": "test_invalid_username", "password": "test_invalid_password"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Incorrect username or password"})