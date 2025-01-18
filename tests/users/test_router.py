import unittest
from fastapi.testclient import TestClient
from main import app

class TestUsersRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_get_users_with_no_users(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_user_by_id_with_no_user(self):
        response = self.client.get("/user/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "User not found"})