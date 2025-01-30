import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

class TestUsersRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    #############################
    # GET - Get a user by user_id test cases

    @patch("src.users.router.get_user_infos")
    def test_get_user_by_id_with_no_auth(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = None
        response = self.client.get("/user/1")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    #############################
    # PUT - Update a user by user_id test cases


    @patch("src.users.router.update_user_in_db")
    @patch("src.auth.router.authenticate_user")
    def test_update_user_with_no_user_and_no_auth(self, mock_update_user_in_db, mock_authenticate_user):
        mock_authenticate_user.return_value = False
        mock_update_user_in_db.return_value = False
        response = self.client.put("/user/", json={"username": "test", "password": "test"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})