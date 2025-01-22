import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

class TestUsersRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    #############################
    # GET - Get all users test cases
        
    @patch("src.users.router.get_users_list")
    def test_get_users_with_no_users(self, mock_get_users_list):
        mock_get_users_list.return_value = []
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "No users found"})

    @patch("src.users.router.get_users_list")
    def test_get_users_with_users(self, mock_get_users_list):
        mock_get_users_list.return_value = [{"id": 1, "username": "test", "followersCount": 0, "followsCount": 0}]
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": 1, "username": "test", "followersCount": 0, "followsCount": 0}])

    #############################
    # GET - Get a user by user_id test cases

    @patch("src.users.router.get_user_infos")
    def test_get_user_by_id_with_no_user(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = None
        response = self.client.get("/user/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "User not found"})

    # TODO: Test à corriger
    # @patch("src.users.router.get_user_infos")
    # @patch("src.sekrets.service.get_secrets_by_user_id")
    # def test_get_user_by_id_with_user(self, mock_get_secrets_by_user_id, mock_get_user_by_id):
    #     mock_get_user_by_id.return_value = {"id": 1, "username": "test", "followersCount": 0, "followsCount": 0}
    #     mock_get_secrets_by_user_id.return_value = []
    #     response = self.client.get("/user/1")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), {"id": 1, "username": "test", "followersCount": 0, "followsCount": 0, "followers": "/user/1/followers", "follows": "/user/1/follows", "secrets": []})

    #############################
    # POST - Create a new user test cases

    @patch("src.users.router.create_user_in_db")
    def test_create_user_with_success(self, mock_create_user_in_db):
        mock_create_user_in_db.return_value = True
        response = self.client.post("/user", json={"username": "test", "password": "test"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "User created"})

    @patch("src.users.router.create_user_in_db")
    def test_create_user_with_username_exists(self, mock_create_user_in_db):
        mock_create_user_in_db.return_value = None
        response = self.client.post("/user", json={"username": "test", "password": "test"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Username already exists"})

    #############################
    # PUT - Update a user by user_id test cases

    @patch("src.users.router.update_user_in_db")
    @patch("src.users.router.authenticate_user")
    def test_update_user_with_success(self, mock_authenticate_user, mock_update_user_in_db):
        # Simuler une authentification réussie
        mock_authenticate_user.return_value = {"id": 1, "username": "test_authenticated_user"}
        # Simuler un succès de la mise à jour
        mock_update_user_in_db.return_value = True

        # Envoyer la requête avec un token simulé
        token = "Bearer mock_valid_token"
        headers = {"Authorization": token}
        payload = {"username": "test_username", "password": "test_password"}

        response = self.client.put("/user/", headers=headers, json=payload)

        # Vérifications
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User updated"})

    @patch("src.users.router.update_user_in_db")
    @patch("src.users.router.authenticate_user")
    def test_update_user_with_no_user_and_no_auth(self, mock_update_user_in_db, mock_authenticate_user):
        mock_authenticate_user.return_value = False
        mock_update_user_in_db.return_value = False
        response = self.client.put("/user/", json={"username": "test", "password": "test"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Unauthorized"})

    #############################
    # DELETE - Delete a user by user_id test cases

    @patch("src.users.router.delete_user_in_db")
    def test_delete_user_with_no_user(self, mock_delete_user_in_db):
        mock_delete_user_in_db.return_value = False
        response = self.client.delete("/user/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "User not found"})

    @patch("src.users.router.delete_user_in_db")
    def test_delete_user_with_success(self, mock_delete_user_in_db):
        mock_delete_user_in_db.return_value = True
        response = self.client.delete("/user/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User deleted"})