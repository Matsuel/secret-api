import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

class TestUsersRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

        
    @patch("src.users.router.get_users_list")
    def test_get_users_with_no_users(self, mock_get_users_list):
        mock_get_users_list.return_value = []
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "No users found"})

    @patch("src.users.router.get_user_by_id")
    def test_get_user_by_id_with_no_user(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = None
        response = self.client.get("/user/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "User not found"})

    @patch("src.users.router.delete_user_in_db")
    def test_delete_user_with_no_user(self, mock_delete_user_in_db):
        mock_delete_user_in_db.return_value = False
        response = self.client.delete("/user/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "User not found"})