import unittest
from fastapi.testclient import TestClient
from main import app

class TestCategoriesRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_get_categories_with_no_categories(self):
        response = self.client.get("/categories")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "No categories found"})
    
    def test_get_category_by_id_with_no_category(self):
        response = self.client.get("/categories/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Category not found"})