import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

class TestSpacesRouter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    #############################
    # GET - Get all spaces test cases

    @patch("src.spaces.router.get_spaces_list")
    def test_get_spaces_with_no_spaces(self, mock_get_spaces_list):
        mock_get_spaces_list.return_value = []
        response = self.client.get("/spaces")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "No spaces found"})

    @patch("src.spaces.router.get_spaces_list")
    def test_get_spaces_with_spaces(self, mock_get_spaces_list):
        mock_get_spaces_list.return_value = [{"id": 1, "name": "test", "is_public": True}]
        response = self.client.get("/spaces")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": 1, "name": "test", "is_public": True}])

    #############################
    # GET - Get a space by space_id test cases

    @patch("src.spaces.router.get_space")
    def test_get_space_by_id_with_no_space(self, mock_get_space):
        mock_get_space.return_value = None
        response = self.client.get("/space/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Space not found"})

    @patch("src.spaces.router.get_space")
    def test_get_space_by_id_with_space(self, mock_get_space):
        mock_get_space.return_value = {"id": 1, "name": "test", "is_public": True}
        response = self.client.get("/space/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "test", "is_public": True})
    
    @patch("src.spaces.router.get_space")
    def test_get_space_by_id_with_invalid_input(self, mock_get_space):
        mock_get_space.return_value = None
        response = self.client.get("/space/invalid_input")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"detail": [{'input': 'invalid_input', 'loc': ['path', 'space_id'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'type': 'int_parsing'}]})

    #############################
    # POST - Create a new space test cases

    @patch("src.spaces.router.create_space")
    def test_create_space_with_success(self, mock_create_space):
        mock_create_space.return_value = True
        response = self.client.post("/space", json={"name": "test", "is_public": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Space created successfully"})

    @patch("src.spaces.router.create_space")
    def test_create_space_with_invalid_data(self, mock_create_space):
        mock_create_space.return_value = None
        response = self.client.post("/space", json={"name": "invalid_data"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"detail": [{"input":{"name": "invalid_data"},"loc": ["body", "is_public"], "msg": "Field required", "type": "missing"}]})

    #############################
    # PUT - Update a space by space_id test cases

    @patch("src.spaces.router.update_space")
    def test_update_space_with_success(self, mock_update_space):
        mock_update_space.return_value = True
        response = self.client.put("/space/1", json={"name": "test", "is_public": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Space updated successfully"})

    @patch("src.spaces.router.update_space")
    def test_update_space_with_no_space(self, mock_update_space):
        mock_update_space.return_value = None
        response = self.client.put("/space/1", json={"name": "test", "is_public": True})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Space not found"})

    @patch("src.spaces.router.update_space")
    def test_update_space_with_invalid_data(self, mock_update_space):
        mock_update_space.return_value = None
        response = self.client.put("/space/1", json={"name": "invalid_data"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"detail": [{"input": {"name": "invalid_data"}, "loc": ["body", "is_public"], "msg": "Field required", "type": "missing"}]})

    #############################
    # PUT - Invite a user in a space test cases

    @patch("src.spaces.router.invite_user_to_space")
    def test_invite_user_in_space_with_success(self, mock_invite_user_in_space):
        mock_invite_user_in_space.return_value = True
        response = self.client.put("/space/1/invite/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User invited successfully"})

    # TODO: Fix this test case
    # @patch("src.spaces.router.invite_user_to_space")
    # def test_invite_user_in_space_with_no_space(self, mock_invite_user_in_space):
    #     mock_invite_user_in_space.return_value = None
    #     response = self.client.put("/space/1/invite/1")
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response.json(), {"detail": "Space not found"})

    #############################
    # DELETE - Delete a space by space_id test cases

    @patch("src.spaces.router.delete_space")
    def test_delete_space_with_success(self, mock_delete_space):
        mock_delete_space.return_value = True
        response = self.client.delete("/space/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Space deleted successfully"})

    @patch("src.spaces.router.delete_space")
    def test_delete_space_with_no_space(self, mock_delete_space):
        mock_delete_space.return_value = None
        response = self.client.delete("/space/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Space not found"})

    @patch("src.spaces.router.delete_space")
    def test_delete_space_with_invalid_input(self, mock_delete_space):
        mock_delete_space.return_value = None
        response = self.client.delete("/space/invalid_input")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"detail": [{'input': 'invalid_input', 'loc': ['path', 'space_id'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'type': 'int_parsing'}]})