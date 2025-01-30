import unittest
from unittest.mock import MagicMock, patch
from src.categories.service import check_if_category_name_exists, create_category_in_db, delete_category_in_db, get_categories_list, get_category_by_id_in_db, update_category_in_db
from src.models.category import CategoryModel

class TestCategoriesService(unittest.TestCase):

    @patch("src.categories.service.SessionLocal")
    def test_get_categories_list(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().offset().limit().all.return_value = ['test_category1', 'test_category2']
        mock_session_local.return_value.__enter__.return_value = mock_session
        response = get_categories_list()
        self.assertEqual(response, ['test_category1', 'test_category2'])

    @patch("src.categories.service.SessionLocal")
    def test_get_categories_list_empty(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().offset().limit().all.return_value = []
        mock_session_local.return_value.__enter__.return_value = mock_session
        response = get_categories_list()
        self.assertEqual(response, [])

    @patch("src.categories.service.SessionLocal")
    def test_get_category_by_id_in_db(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = 'test_category'
        mock_session_local.return_value.__enter__.return_value = mock_session
        response = get_category_by_id_in_db(1)
        self.assertEqual(response, 'test_category')

    @patch("src.categories.service.SessionLocal")
    def test_get_category_by_id_in_db_empty(self, mock_session_local):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session
        response = get_category_by_id_in_db(1)
        self.assertEqual(response, None)

    @patch("src.categories.service.SessionLocal")
    def test_check_if_category_name_exists_true(self, mock_session_local):
        mock_session= MagicMock()
        mock_session.query().filter().first.return_value = 'test_category'
        mock_session_local.return_value.__enter__.return_value = mock_session
        response = check_if_category_name_exists('test_category')
        self.assertEqual(response, True)

    @patch("src.categories.service.SessionLocal")
    def test_check_if_category_name_exists_false(self, mock_session_local):
        mock_session= MagicMock()
        mock_session.query().filter().first.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session
        response = check_if_category_name_exists('test_category')
        self.assertEqual(response, False)
    
    @patch("src.categories.service.SessionLocal")
    def test_create_category_in_db(self, mock_session_local):
        category = CategoryModel(
            id=1,
            name='test_category'
        )
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = None
        mock_session_local.return_value.__enter__.return_value = mock_session
        response = create_category_in_db(category=category)
        self.assertEqual(response, True)

    @patch("src.categories.service.SessionLocal")
    def test_create_category_in_db_exists(self, mock_session_local):
        category = CategoryModel(
            id=1,
            name='test_category'
        )
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = 'test_category'
        mock_session_local.return_value.__enter__.return_value = mock_session
        response = create_category_in_db(category=category)
        self.assertEqual(response, None)

    @patch("src.categories.service.SessionLocal")
    @patch("src.categories.service.get_category_by_id_in_db")
    @patch("src.categories.service.check_if_category_name_exists")
    def test_update_category_in_db(self, mock_check_name_exists, mock_get_category_by_id, mock_session_local):
        mock_get_category_by_id.return_value = True
        mock_check_name_exists.return_value = False
        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        updated_category = MagicMock(name="test_updated_category")
        response = update_category_in_db(1, updated_category)
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        self.assertTrue(response)

    @patch("src.categories.service.SessionLocal")
    def test_delete_category_in_db(self, mock_session_local):
        category = CategoryModel(
            id=1,
            name='test_category'
        )
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = category
        mock_session_local.return_value.__enter__.return_value = mock_session
        create_category_in_db(category)
        mock_session.commit = MagicMock()
        result = delete_category_in_db(1)
        mock_session.commit.assert_called_once()
        self.assertTrue(result)