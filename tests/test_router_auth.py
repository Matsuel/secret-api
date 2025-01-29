import unittest
from unittest.mock import patch
from src.auth.service import authenticate_user, create_access_token
from src.users.service import authenticate_user, create_access_token
class TestAuthService(unittest.TestCase):
    @patch("src.auth.service.get_user_from_db")
    def test_authenticate_user_success(self, mock_get_user):
        mock_get_user.return_value = {
            "id": 1,
            "username": "test",
            "hashed_password": "hashed_test"
        }
        user = authenticate_user("test", "test_password")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "test")
    
    @patch("src.auth.service.get_user_from_db")
    def test_authenticate_user_failure(self, mock_get_user):
        mock_get_user.return_value = None
        user = authenticate_user("invalid_user", "invalid_password")
        self.assertIsNone(user)
    
    def test_create_access_token(self):
        user = {"id": 1, "username": "test"}
        token = create_access_token(user)
        self.assertIsNotNone(token)