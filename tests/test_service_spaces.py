import unittest
from unittest.mock import patch, MagicMock
from src.spaces.service import delete_space, get_spaces_list, get_space

class TestSpacesService(unittest.TestCase):

    #############################
    # GET - Get all spaces test cases

    @patch("src.spaces.service.SessionLocal")
    def test_get_spaces_list_empty(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().all.return_value = []
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_spaces_list()
        self.assertEqual(result, [])

    # TODO: Valeur de retour à modifier
    @patch("src.spaces.service.SessionLocal")
    def test_get_spaces_list(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().all.return_value = [MagicMock()]
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_spaces_list()
        self.assertNotEqual(result, [])

    #############################
    # GET - Get a space by space_id test cases

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
    # DELETE - Delete a space test cases

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