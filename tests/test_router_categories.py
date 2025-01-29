import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

class TestCategoriesRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    #############################
    # GET - Get all categories test cases

    @patch("src.categories.router.get_categories_list")
    def test_get_categories_with_no_categories(self, mock_get_categories_list):
        mock_get_categories_list.return_value = []
        response = self.client.get("/categories")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "No categories found"})

    @patch("src.categories.router.get_categories_list")
    def test_get_categories_with_categories(self, mock_get_categories_list):
        mock_get_categories_list.return_value = [{"id": 1, "name": "test"}]
        response = self.client.get("/categories")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": 1, "name": "test"}])
        
    @patch("src.categories.router.get_categories_list")
    def test_get_categories_with_no_auth(self, mock_get_categories_list):
        mock_get_categories_list.return_value = None
        response = self.client.get("/categories")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    #############################
    # GET - Get a category by category_id test cases
    
    @patch("src.categories.router.get_category_by_id_in_db")
    def test_get_category_by_id_with_no_category(self, mock_get_category_by_id_in_db):
        mock_get_category_by_id_in_db.return_value = None
        response = self.client.get("/categories/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Category not found"})

    @patch("src.categories.router.get_category_by_id_in_db")
    def test_get_category_by_id_with_category(self, mock_get_category_by_id_in_db):
        mock_get_category_by_id_in_db.return_value = {"id": 1, "name": "test"}
        response = self.client.get("/categories/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "test"})
        
    @patch("src.categories.router.get_category_by_id_in_db")
    def test_get_category_by_id_with_no_auth(self, mock_get_category_by_id_in_db):
        mock_get_category_by_id_in_db.return_value = None
        response = self.client.get("/categories/1")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    #############################
    # POST - Create a new category test cases   

    @patch("src.categories.router.create_category_in_db")
    def test_create_category_with_success(self, mock_create_category_in_db):
        mock_create_category_in_db.return_value = True
        response = self.client.post("/categories", json={"id":0, "name": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Category created"})
        
    @patch("src.categories.router.create_category_in_db")
    def test_create_category_with_no_auth(self, mock_create_category_in_db):
        mock_create_category_in_db.return_value = True
        response = self.client.post("/categories", json=None)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    @patch("src.categories.router.create_category_in_db")
    def test_create_category_with_category_exists(self, mock_create_category_in_db):
        mock_create_category_in_db.return_value = None
        response = self.client.post("/categories", json={"id":0, "name": "test"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Category already exists"})

    #############################
    # PUT - Update a category by category_id test cases

    @patch("src.categories.router.update_category_in_db")
    def test_update_category_with_success(self, mock_update_category_in_db):
        mock_update_category_in_db.return_value = True
        response = self.client.put("/categories/1", json={"name": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Category updated"})
        
    @patch("src.categories.router.update_category_in_db")
    def test_update_category_with_no_auth(self, mock_update_category_in_db):
        mock_update_category_in_db.return_value = True
        response = self.client.put("/categories/1", json=None)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    @patch("src.categories.router.update_category_in_db")
    def test_update_category_with_invalid_input(self, mock_update_category_in_db):
        mock_update_category_in_db.return_value = None
        response = self.client.put("/categories/1", json={"name": "test_invalid"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Category not found or name already exists"})

    #############################
    # DELETE - Delete a category by category_id test cases

    @patch("src.categories.router.delete_category_in_db")
    def test_delete_category_with_success(self, mock_delete_category_in_db):
        mock_delete_category_in_db.return_value = True
        response = self.client.delete("/categories/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Category deleted"})
        
    @patch("src.categories.router.delete_category_in_db")
    def test_delete_category_with_no_auth(self, mock_delete_category_in_db):
        mock_delete_category_in_db.return_value = True
        response = self.client.delete("/categories/1")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    @patch("src.categories.router.delete_category_in_db")
    def test_delete_category_with_no_category(self, mock_delete_category_in_db):
        mock_delete_category_in_db.return_value = False
        response = self.client.delete("/categories/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Category not found"})