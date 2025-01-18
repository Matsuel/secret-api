import unittest
from fastapi.testclient import TestClient
from main import app

class TestSpacesRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_get_spaces_with_no_spaces(self):
        response = self.client.get("/spaces")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_space_by_id_with_no_space(self):
        response = self.client.get("/space/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)