import unittest
from unittest.mock import patch, MagicMock

import bcrypt
from src.users.service import authenticate_user, delete_user_in_db, get_user_by_id, get_user_infos, get_users_list, hash_password, update_user_in_db, verify_password, create_user_in_db, check_if_user_exists
from src.models.user import User


class TestUserService(unittest.TestCase):

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

    @patch("src.users.service.SessionLocal")
    def test_get_user_infos(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_user_infos(1)
        self.assertIsNotNone(result)

    @patch("src.users.service.SessionLocal")
    def test_get_user_by_id_none(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_user_by_id(1)
        self.assertIsNone(result)

    @patch("src.users.service.SessionLocal")
    def test_get_users_list(self, mock_session_local):
        user1 = User(username="test_username", password="test_password")
        user2 = User(username="test_username2", password="test_password2")
        mock_session = MagicMock()
        mock_session.query().offset().limit().all.return_value = [user1, user2]
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_users_list()
        self.assertEqual(len(result), 2)

    @patch("src.users.service.SessionLocal")
    def test_get_users_list_empty(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().offset().limit().all.return_value = []
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_users_list()
        self.assertEqual(result, [])

    @patch("src.users.service.SessionLocal")
    def test_check_if_user_exists(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().get.return_value = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = check_if_user_exists(1)
        self.assertTrue(result)

    @patch("src.users.service.SessionLocal")
    def test_check_if_user_exists_false(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().get.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = check_if_user_exists(1)
        self.assertFalse(result)

    @patch("src.users.service.SessionLocal")
    def test_delete_user_in_db(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().get.return_value = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = delete_user_in_db(1)
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        self.assertTrue(result)

    @patch("src.users.service.SessionLocal")
    def test_delete_user_in_db_false(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().get.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = delete_user_in_db(1)
        self.assertFalse(result)
    
    @patch("src.users.service.SessionLocal")
    @patch("src.users.service.check_if_user_exists")
    @patch("src.users.service.check_username_exists")
    @patch("src.users.service.hash_password")
    def test_update_user_in_db(self, mock_hash_password, mock_check_username_exists, mock_check_if_user_exists, mock_session_local):
        
        mock_check_if_user_exists.return_value = True
        mock_check_username_exists.return_value = False
        mock_hash_password.return_value = "hashed_password"
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        
        user = User(
            username="test_new_username",
            password="test_new_password"
            )
        result = update_user_in_db(1, user)
        
        mock_check_if_user_exists.assert_called_once_with(1)
        mock_check_username_exists.assert_called_once_with("test_new_username")
        mock_hash_password.assert_called_once_with("test_new_password")
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        
        self.assertTrue(result)

    @patch("src.users.service.SessionLocal")
    @patch("src.users.service.check_if_user_exists")
    def test_update_user_in_db_user_not_exists(self, mock_check_if_user_exists, mock_session_local):
        
        mock_check_if_user_exists.return_value = False
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        
        user = User(
            username="test_new_username",
            password="test_new_password"
            )
        result = update_user_in_db(1, user)
        
        mock_check_if_user_exists.assert_called_once_with(1)
        self.assertFalse(result)

    @patch("src.users.service.SessionLocal")
    @patch("src.users.service.check_if_user_exists")
    def test_update_user_in_db_username_exists(self, mock_check_if_user_exists, mock_session_local):
        
        mock_check_if_user_exists.return_value = True
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        
        user = User(
            username="test_new_username",
            password="test_new_password"
            )
        result = update_user_in_db(1, user)
        
        mock_check_if_user_exists.assert_called_once_with(1)
        self.assertFalse(result)

    @patch("src.users.service.SessionLocal")
    @patch("src.users.service.verify_password")
    def test_authenticate_user(self, mock_session_local, mock_verify_password):
        plain_password = "test_password"
        hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
        mock_user = MagicMock()
        mock_user.password = hashed_password.decode("utf-8")
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = mock_user
        mock_session_local.return_value.__enter__.return_value = mock_session
        mock_verify_password.return_value = True

        result = authenticate_user("test_username", plain_password, mock_session)

        self.assertIsNotNone(result)

    @patch("src.users.service.SessionLocal")
    @patch("src.users.service.verify_password")
    def test_authenticate_user_user_not_found(self, mock_session_local, mock_verify_password):
        plain_password = "test_password"
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session
        mock_verify_password.return_value = True

        result = authenticate_user("test_username", plain_password, mock_session)

        self.assertIsNone(result)

    @patch("src.users.service.SessionLocal")
    @patch("src.users.service.verify_password")
    def test_authenticate_user_wrong_password(self, mock_verify_password, mock_session_local):
        plain_password = "test_password"
        hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
        mock_user = MagicMock()
        mock_user.password = hashed_password.decode("utf-8")
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = mock_user
        mock_session_local.return_value.__enter__.return_value = mock_session
        mock_verify_password.return_value = False

        result = authenticate_user("test_username", "wrong_password", mock_session)

        mock_verify_password.assert_called_once_with("wrong_password", mock_user.password)
        self.assertIsNone(result)
