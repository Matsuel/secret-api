import unittest
from unittest.mock import patch, MagicMock
from src.spaces.service import create_space, delete_space, get_spaces_list, get_space, update_space, accept_invitation

class TestSpacesService(unittest.TestCase):

    #############################
    # get_spaces_list() test cases

    @patch("src.spaces.service.SessionLocal")
    def test_get_spaces_list_empty(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().all.return_value = []
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_spaces_list()
        self.assertEqual(result, [])

    @patch("src.spaces.service.SessionLocal")
    def test_get_spaces_list(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().all.return_value = [MagicMock()]
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_spaces_list()
        self.assertNotEqual(result, [])

    #############################
    # get_space(space_id: int)  test cases

    @patch("src.spaces.service.SessionLocal")
    def test_get_space_by_id_none(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = []
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_space(1)
        self.assertIsNone(result)

    @patch("src.spaces.service.SessionLocal")
    def test_get_space_by_id(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_space(1)
        self.assertIsNotNone(result)

    #############################
    # delete_space(space_id: int) test cases

    @patch("src.spaces.service.SessionLocal")
    def test_delete_space(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = delete_space(1)
        self.assertIsNotNone(result)

    @patch("src.spaces.service.SessionLocal")
    def test_delete_space_none(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = []
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = delete_space(1)
        self.assertIsNone(result)


    @patch("src.spaces.service.SessionLocal")
    def test_update_space(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = update_space(1)
        self.assertIsNotNone(result)

    @patch("src.spaces.service.SessionLocal")
    def test_update_space_none(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = []
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = update_space(1)
        self.assertIsNone(result)

    @patch("src.spaces.service.SessionLocal")
    def test_create_space(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().order_by().first.return_value = [1]
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = create_space('test_space', True)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'test_space')
        self.assertEqual(result.is_public, True)

    @patch("src.spaces.service.SessionLocal")
    def test_accept_invitation(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = accept_invitation(1, 1)
        self.assertIsNotNone(result)

    @patch("src.spaces.service.SessionLocal")
    def test_accept_invitation_none(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = []
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = accept_invitation(1, 1)
        self.assertIsNone(result)