import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

class TestSekretRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    #############################
    # POST - Create a new secret test cases

    @patch("src.sekrets.router.create_secret_db")
    def test_create_sekret_with_invalid_data(self, mock_create_secret_db):
        mock_create_secret_db.return_value = False
        response = self.client.post("/secret", json={"text": "test_create_invalid_data", "user_id": 0, "category_id": 0, "is_public": True, "shared_space_id": 0, "anonymous": True, "likesCount": 0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Error creating secret"})

    @patch("src.sekrets.router.create_secret_db")
    def test_create_sekret_with_no_user(self, mock_create_secret_db):
        mock_create_secret_db.return_value = "Utilisateur non trouvé"
        response = self.client.post("/secret", json={"text": "test_create_no_user", "user_id": 0, "category_id": 0, "is_public": True, "shared_space_id": 0, "anonymous": True, "likesCount": 0})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Utilisateur non trouvé"})

    @patch("src.sekrets.router.create_secret_db")
    def test_create_sekret(self, mock_create_secret_db):
        mock_create_secret_db.return_value = True
        response = self.client.post("/secret", json={"text": "test_create_valid", "user_id": 1, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 0})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Secret created successfully"})

    #############################
    # GET - Get all secrets test cases

    @patch("src.sekrets.router.get_all_secrets_from_db")
    def test_get_sekrets_with_no_sekrets(self, mock_get_all_secrets_from_db):
        mock_get_all_secrets_from_db.return_value = []
        response = self.client.get("/secrets")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "No secrets found"})

    @patch("src.sekrets.router.get_all_secrets_from_db")
    def test_get_sekrets_with_sekrets(self, mock_get_all_secrets_from_db):
        mock_get_all_secrets_from_db.return_value = [{"id": 1, "text": "test", "user_id": 1, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 0}, {"id": 2, "text": "test", "user_id": 1, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 0}]
        response = self.client.get("/secrets")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": 1, "text": "test", "user_id": 1, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 0}, {"id": 2, "text": "test", "user_id": 1, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 0}])

    #############################
    # GET - Get a secret by secret_id test cases

    @patch("src.sekrets.router.get_secret_by_id")
    def test_get_sekret_by_id_with_no_sekret(self, mock_get_secret_by_id):
        mock_get_secret_by_id.return_value = None
        response = self.client.get("/secret/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Secret not found"})

    @patch("src.sekrets.router.get_secret_by_id")
    def test_get_sekret_by_id_with_sekret(self, mock_get_secret_by_id):
        mock_get_secret_by_id.return_value = {"id": 1, "text": "test", "user_id": 1, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 0}
        response = self.client.get("/secret/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "text": "test", "user_id": 1, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 0})

    @patch("src.sekrets.router.get_secret_by_id")
    def test_get_sekret_by_id_with_invalid_input(self, mock_get_secret_by_id):
        mock_get_secret_by_id.return_value = None
        response = self.client.get("/secret/invalid_input")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': [{'input': 'invalid_input', 'loc': ['path', 'secret_id'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'type': 'int_parsing'}]})

    #############################
    # GET - Get secret by space_id test cases

    @patch("src.sekrets.router.get_secrets_by_space_id")
    def test_get_sekrets_by_space_id_with_no_sekrets(self, mock_get_secrets_by_space_id):
        mock_get_secrets_by_space_id.return_value = None
        response = self.client.get("/secret/space/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Secret not found"})

    @patch("src.sekrets.router.get_secrets_by_space_id")
    def test_get_sekrets_by_space_id_with_sekrets(self, mock_get_secrets_by_space_id):
        mock_get_secrets_by_space_id.return_value = {"id": 1, "text": "test", "user_id": 1, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 0}
        response = self.client.get("/secret/space/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "text": "test", "user_id": 1, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 0})

    @patch("src.sekrets.router.get_secrets_by_space_id")
    def test_get_sekrets_by_space_id_with_invalid_input(self, mock_get_secrets_by_space_id):
        mock_get_secrets_by_space_id.return_value = None
        response = self.client.get("/secret/space/invalid_input")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': [{'input': 'invalid_input', 'loc': ['path', 'space_id'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'type': 'int_parsing'}]})

    #############################
    # PUT - Update a secret by secret_id test cases

    @patch("src.sekrets.router.update_secret_in_db")
    def test_update_sekret_with_no_sekret(self, mock_update_secret_in_db):
        mock_update_secret_in_db.return_value = False
        response = self.client.put("/secret/1", json={"text": "test_update_no_secret", "is_public": True, "anonymous": False, "category_id": 1, "shared_space_id": 1})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Secret not found"})

    @patch("src.sekrets.router.update_secret_in_db")
    def test_update_sekret(self, mock_update_secret_in_db):
        mock_update_secret_in_db.return_value = True
        response = self.client.put("/secret/1", json={"text": "test_update_valid", "is_public": True, "anonymous": False, "category_id": 1, "shared_space_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Secret updated successfully", "data": {"text": "test_update_valid", "is_public": True, "anonymous": False, "category_id": 1, "shared_space_id": 1}})

    @patch("src.sekrets.router.update_secret_in_db")
    def test_update_sekret_with_invalid_input(self, mock_update_secret_in_db):
        mock_update_secret_in_db.return_value = False
        response = self.client.put("/secret/invalid_input", json={"text": "test_update_invalid_input", "is_public": True, "anonymous": False, "category_id": 1, "shared_space_id": 1})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': [{'input': 'invalid_input', 'loc': ['path', 'secret_id'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'type': 'int_parsing'}]})

    #############################
    # DELETE - Delete a secret by id test cases

    @patch("src.sekrets.router.delete_secret_in_db")
    def test_delete_sekret_with_no_sekret(self, mock_delete_secret_in_db):
        mock_delete_secret_in_db.return_value = False
        response = self.client.delete("/secret/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Secret not found"})

    @patch("src.sekrets.router.delete_secret_in_db")
    def test_delete_sekret(self, mock_delete_secret_in_db):
        mock_delete_secret_in_db.return_value = True
        response = self.client.delete("/secret/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Secret deleted successfully"})

    @patch("src.sekrets.router.delete_secret_in_db")
    def test_delete_sekret_with_invalid_input(self, mock_delete_secret_in_db):
        mock_delete_secret_in_db.return_value = False
        response = self.client.delete("/secret/invalid_input")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': [{'input': 'invalid_input', 'loc': ['path', 'secret_id'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'type': 'int_parsing'}]})

    #############################
    # POST - Like a secret by secret_id test cases

    @patch("src.sekrets.router.like_secret_in_db")
    def test_like_sekret_with_no_sekret(self, mock_like_secret_in_db):
        mock_like_secret_in_db.return_value = False
        response = self.client.post("/secret/1/like")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Secret not found"})
    
    @patch("src.sekrets.router.like_secret_in_db")
    def test_like_sekret(self, mock_like_secret_in_db):
        mock_like_secret_in_db.return_value = True
        response = self.client.post("/secret/1/like")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Secret liked successfully"})

    @patch("src.sekrets.router.like_secret_in_db")
    def test_like_sekret_with_invalid_input(self, mock_like_secret_in_db):
        mock_like_secret_in_db.return_value = False
        response = self.client.post("/secret/invalid_input/like")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': [{'input': 'invalid_input', 'loc': ['path', 'secret_id'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'type': 'int_parsing'}]})

    #############################
    # GET - secrets popular test cases

    @patch("src.sekrets.router.update_secret_in_db")
    def test_get_sekrets_popular_with_no_sekrets(self, mock_update_secret_in_db):
        mock_update_secret_in_db.return_value = False
        response = self.client.get("/secrets/popular")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])