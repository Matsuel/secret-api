import unittest
from unittest.mock import patch, MagicMock
from src.sekrets.service import create_secret_db, get_all_secrets_from_db, get_secret_by_id, get_secrets_by_space_id, get_secrets_by_user_id, like_secret_in_db, delete_secret_in_db, update_secret_in_db
from src.models.secret import CreateSecret

class TestSekretsService(unittest.TestCase):

    #############################
    # create_secret_db(secret: CreateSecret) test cases

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
        result = create_secret_db(sekret)
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        self.assertTrue(result)

    #############################
    # get_secret_by_id(secret_id: int) test cases

    @patch("src.sekrets.service.SessionLocal")
    def test_get_secret_by_id_true(self, mock_session_local):
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
        mock_session.query().filter().first.return_value = sekret
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_secret_by_id(1)
        self.assertEqual(result, sekret)

    @patch("src.sekrets.service.SessionLocal")
    def test_get_secret_by_id_false(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_secret_by_id(1)
        self.assertEqual(result, None)

    #############################
    # get_all_secrets_from_db(offset: int = 0, limit: int = 100) test cases

    @patch("src.sekrets.service.SessionLocal")
    def test_get_all_secrets_from_db_true(self, mock_session_local):
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
        mock_session.query().offset().limit().all.return_value = [sekret,sekret]
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_all_secrets_from_db()
        self.assertEqual(result, [sekret,sekret])

    @patch("src.sekrets.service.SessionLocal")
    def test_get_all_secrets_from_db_false(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().offset().limit().all.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_all_secrets_from_db()
        self.assertEqual(result, None)

    #############################
    # get_secrets_by_space_id(space_id: int) test cases

    @patch("src.sekrets.service.SessionLocal")
    def test_get_secrets_by_space_id_true(self, mock_session_local):
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
        mock_session.query().filter().first.return_value = sekret
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_secrets_by_space_id(1)
        self.assertEqual(result, sekret)

    @patch("src.sekrets.service.SessionLocal")
    def test_get_secrets_by_space_id_false(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_secrets_by_space_id(1)
        self.assertEqual(result, None)

    #############################
    # get_secrets_by_user_id(user_id: int) test cases

    @patch("src.sekrets.service.SessionLocal")
    def test_get_secrets_by_user_id_true(self, mock_session_local):
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
        mock_session.query().filter().all.return_value = [sekret,sekret]
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_secrets_by_user_id(1)
        self.assertEqual(result, [sekret,sekret])

    @patch("src.sekrets.service.SessionLocal")
    def test_get_secrets_by_user_id_false(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().all.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_secrets_by_user_id(1)
        self.assertEqual(result, None)

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
        create_secret_db(sekret)
        mock_session.commit = MagicMock()
        mock_session.execute.reset_mock()
        sekret.text = "new_text"
        result = update_secret_in_db(1, sekret)
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
        create_secret_db(sekret)
        mock_session.commit = MagicMock()
        result = delete_secret_in_db(1)
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
        create_secret_db(sekret)
        mock_session.commit = MagicMock()
        result = like_secret_in_db(1)
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        self.assertTrue(result)
