import unittest
from unittest.mock import patch, MagicMock
from src.sekrets.service import create_secret_db, like_secret_in_db, delete_secret_in_db, update_secret_in_db
from src.models.secret import CreateSecret

class TestSekretsService(unittest.TestCase):

    #############################
    # create_secret_db(secret: CreateSecret, user_id: int) test cases

    @patch("src.sekrets.service.SessionLocal")
    def test_create_sekret_in_db(self, mock_session_local):
        sekret = CreateSecret(
            text="test_text",
            user_id=1,
            category_id=1,
            is_public=True,
            shared_space_id=1,
            anonymous=True,
            likesCount=1
        )
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = create_secret_db(sekret, sekret.user_id)
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        self.assertTrue(result)

    #############################
    # like_secret_in_db(secret_id: int) test cases

    @patch("src.sekrets.service.SessionLocal")
    def test_like_secret_in_db(self, mock_session_local):
        sekret = CreateSecret(
            text="test_text",
            user_id=1,
            category_id=1,
            is_public=True,
            shared_space_id=1,
            anonymous=True,
            likesCount=1
        )
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        create_secret_db(sekret, sekret.user_id)
        mock_session.commit = MagicMock()
        result = like_secret_in_db(1)
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        self.assertTrue(result)

    #############################
    # delete_secret_in_db(secret_id: int) test cases

    @patch("src.sekrets.service.SessionLocal")
    def test_delete_secret_in_db(self, mock_session_local):
        sekret = CreateSecret(
            text="test_text",
            user_id=1,
            category_id=1,
            is_public=True,
            shared_space_id=1,
            anonymous=True,
            likesCount=1
        )
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        create_secret_db(sekret, sekret.user_id)
        mock_session.commit = MagicMock()
        result = delete_secret_in_db(1)
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        self.assertTrue(result)

    #############################
    # update_secret_in_db(secret_id: int, secret: Secret) test cases

    @patch("src.sekrets.service.SessionLocal")
    def test_update_secret_in_db(self, mock_session_local):
        sekret = CreateSecret(
            text="test_text",
            user_id=1,
            category_id=1,
            is_public=True,
            shared_space_id=1,
            anonymous=True,
            likesCount=1
        )
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        create_secret_db(sekret, sekret.user_id)
        mock_session.commit = MagicMock()
        mock_session.execute.reset_mock()
        sekret.text = "new_text"
        result = update_secret_in_db(1, sekret)
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        self.assertTrue(result)