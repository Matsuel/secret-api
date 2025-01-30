import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

class TestFollowersRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    #############################
    # GET - Get all follows of a user by user_id test cases
        
    @patch("src.followers.router.get_follows_in_db")
    def test_get_user_follows_with_no_auth(self, mock_get_follows_in_db):
        mock_get_follows_in_db.return_value = [{"id": 1, "username": "test", "followersCount": 0, "followsCount": 0}]
        response = self.client.get("/user/1/follow")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'detail': 'Not authenticated'})

    #############################
    # GET - Get all followers of a user by user_id test cases
        
    @patch("src.followers.router.get_followers_in_db")
    def test_get_user_followers_with_no_auth(self, mock_get_followers_in_db):
        mock_get_followers_in_db.return_value = [{"id": 1, "username": "test", "followersCount": 0, "followsCount": 0}]
        response = self.client.get("/user/1/followers")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'detail': 'Not authenticated'})

    ############################
    # POST - Follow a user test cases

    @patch("src.followers.router.follow_user_in_db")
    def test_follow_user_with_invalid_input(self, mock_follow_user_in_db):
        mock_follow_user_in_db.return_value = None
        response = self.client.post("/user/1/follow/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Not Found"})
        