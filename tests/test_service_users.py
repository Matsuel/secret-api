import unittest
from unittest.mock import patch, MagicMock
from src.users.service import get_user_by_id, hash_password, verify_password, create_user_in_db
from src.models.user import User


class TestCreateUserInDB(unittest.TestCase):
    @patch("src.users.service.check_username_exists")
    @patch("src.users.service.hash_password")
    @patch("src.users.service.SessionLocal")
    def test_create_user_in_db(self, mock_session_local, mock_hash_password, mock_check_username_exists):
        user = User(username="test_username", password="test_password")
        mock_check_username_exists.return_value = False
        mock_hash_password.return_value = "hashed_password"
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = create_user_in_db(user)
        mock_check_username_exists.assert_called_once_with("test_username")
        mock_hash_password.assert_called_once_with("test_password")
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        self.assertTrue(result)

    @patch("src.users.service.check_username_exists")
    def test_check_username_exists(self, mock_check_username_exists):
        user = User(username="test_username", password="test_password")
        mock_check_username_exists.return_value = True
        result = create_user_in_db(user)
        mock_check_username_exists.assert_called_once_with("test_username")
        self.assertIsNone(result)

    def test_hash_password(self):
        password = "test_password"
        hashed_password = hash_password(password)
        self.assertNotEqual(password, hashed_password)

    def test_verify_password(self):
        password = "test_password"
        hashed_password = hash_password(password)
        self.assertTrue(verify_password(password, hashed_password))
        self.assertFalse(verify_password("wrong_password", hashed_password))

    @patch("src.users.service.SessionLocal")
    def test_get_user_by_id(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_user_by_id(1)
        self.assertIsNotNone(result)