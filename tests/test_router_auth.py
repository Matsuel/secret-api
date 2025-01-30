import unittest
from unittest.mock import Mock, patch
from src.auth.service import authenticate_user, create_access_token
from src.models.user import User

class TestAuthService(unittest.TestCase):

    @patch("src.auth.service.verify_token")
    @patch("src.auth.service.get_user_by_id")
    def test_authenticate_user_success(self, mock_get_user_by_id, mock_verify_token):
        mock_verify_token.return_value = {"user_id": 1}
        mock_user = Mock()
        mock_user.username = "test"
        mock_get_user_by_id.return_value = mock_user
        token = "valid_token"
        result = authenticate_user(token)
        self.assertIsNotNone(result)
        self.assertEqual(result.username, "test")

    @patch("src.auth.service.verify_token")
    def test_authenticate_user_failure(self, mock_verify_token):
        mock_verify_token.return_value = None
        invalid_token = "invalid_token"
        result = authenticate_user(invalid_token)
        self.assertFalse(result)
    
    def test_create_access_token(self):
        user = {"id": 1, "username": "test"}
        user = User(
            id = 1,
            username = "test",
            password = "test_password"
        )
        token = create_access_token(user)
        self.assertIsNotNone(token)