import unittest
from unittest.mock import patch, MagicMock
from src.categories.service import (
    create_category_in_db,
    get_category_by_id_in_db,
    update_category_in_db,
    delete_category_in_db
)
from src.models.category import CategoryModel, CategoryEdit
class TestServiceCategoriesExtended(unittest.TestCase):
    @patch("src.categories.service.check_if_category_name_exists")
    @patch("src.categories.service.SessionLocal")
    def test_create_category_in_db(self, mock_session_local, mock_check_name):
        mock_check_name.return_value = False
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = create_category_in_db(CategoryModel(id=1, name="test"))
        mock_check_name.assert_called_once_with("test")
        self.assertTrue(result)

    @patch("src.categories.service.SessionLocal")
    def test_get_category_by_id_in_db(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = {"id": 1, "name": "test"}
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = get_category_by_id_in_db(1)
        self.assertEqual(result["id"], 1)

    @patch("src.categories.service.SessionLocal")
    def test_delete_category_in_db(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = {"id": 1, "name": "to_delete"}
        mock_session_local.return_value.__enter__.return_value = mock_session
        result = delete_category_in_db(1)
        self.assertTrue(result)