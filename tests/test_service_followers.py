import unittest
from unittest.mock import patch, MagicMock
from src.followers.service import follow_user_in_db, get_follows_in_db, get_followers_in_db, is_following, unfollow_user_in_db
from src.models.follower import Follower

class TestFollowersService(unittest.TestCase):

    #############################
    # follow_user_in_db(user_id: int, user_to_follow_id: int) test cases

    @patch("src.followers.service.SessionLocal")
    def test_follow_user_success(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None  # L'utilisateur existe et ne suit pas déjà

        result = follow_user_in_db(1, 2)

        # Vérifier que 'execute' a été appelé trois fois
        self.assertEqual(mock_session.execute.call_count, 3, "La méthode 'execute' a été appelée 3 fois au lieu d'une seule.")

        mock_session.commit.assert_called_once()
        self.assertTrue(result)

    @patch("src.followers.service.SessionLocal")
    def test_unfollow_user_success(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = Follower(user_id=1, follower_id=2)

        result = unfollow_user_in_db(1, 2)

        # Vérifier que 'execute' a été appelé deux fois
        self.assertEqual(mock_session.execute.call_count, 2, "La méthode 'execute' a été appelée 2 fois au lieu d'une seule.")

        mock_session.commit.assert_called_once()
        self.assertTrue(result)

    @patch("src.followers.service.SessionLocal")
    def test_follow_user_nonexistent_user(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None  # Utilisateur à suivre inexistant

        result = follow_user_in_db(1, 999)

        mock_session.execute.assert_not_called()
        mock_session.commit.assert_not_called()
        self.assertIsNone(result)

    @patch("src.followers.service.SessionLocal")
    def test_follow_user_self_follow(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session

        result = follow_user_in_db(1, 1)

        mock_session.execute.assert_not_called()
        mock_session.commit.assert_not_called()
        self.assertIsNone(result)

    #############################
    # get_follows_in_db(user_id: int, offset: int = 0, limit: int = 100) test cases

    @patch("src.followers.service.SessionLocal")
    def test_get_follows_with_follows(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [
            Follower(user_id=1, follower_id=2),
            Follower(user_id=1, follower_id=3)
        ]
        mock_session_local.return_value.__enter__.return_value = mock_session

        result = get_follows_in_db(1)

        mock_session.query.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].follower_id, 2)
        self.assertEqual(result[1].follower_id, 3)

    @patch("src.followers.service.SessionLocal")
    def test_get_follows_with_no_follows(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        mock_session_local.return_value.__enter__.return_value = mock_session

        result = get_follows_in_db(1)

        mock_session.query.assert_called_once()
        self.assertIsNone(result)

    #############################
    # get_followers_in_db(user_id: int, offset: int = 0, limit: int = 100) test cases

    @patch("src.followers.service.SessionLocal")
    def test_get_followers_with_followers(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [
            Follower(user_id=2, follower_id=1),
            Follower(user_id=3, follower_id=1)
        ]
        mock_session_local.return_value.__enter__.return_value = mock_session

        result = get_followers_in_db(1)

        mock_session.query.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].user_id, 2)
        self.assertEqual(result[1].user_id, 3)

    @patch("src.followers.service.SessionLocal")
    def test_get_followers_with_no_followers(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        mock_session_local.return_value.__enter__.return_value = mock_session

        result = get_followers_in_db(1)

        mock_session.query.assert_called_once()
        self.assertIsNone(result)

    #############################
    # is_following(user_id: int, followed_id: int) test cases

    @patch("src.followers.service.SessionLocal")
    def test_is_following_true(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = Follower(user_id=1, follower_id=2)
        mock_session_local.return_value.__enter__.return_value = mock_session

        result = is_following(1, 2)

        mock_session.query.assert_called_once()
        self.assertTrue(result)

    @patch("src.followers.service.SessionLocal")
    def test_is_following_false(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session

        result = is_following(1, 3)

        mock_session.query.assert_called_once()
        self.assertFalse(result)