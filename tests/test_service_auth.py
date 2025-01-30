import asyncio
import unittest
from unittest.mock import patch, MagicMock

from fastapi import HTTPException

from src.models.user import User
from src.auth.service import authenticate_user, create_access_token, get_user, verify_token, get_current_user

class TestAuthService(unittest.TestCase):
    
    def test_create_access_token(self):
        user = User(
            username='test_user',
            password='test_password'
        )
        result = create_access_token(user)
        self.assertIsNotNone(result)

    def test_verify_token_valid(self):
        token = create_access_token(User(
            username='test_user',
            password='test_password'
        ))
        result = verify_token(token)
        self.assertIsNotNone(result)

    def test_verify_token_invalid(self):
        token = 'test_invalid_token'
        with self.assertRaises(HTTPException) as e:
            verify_token(token)
        self.assertEqual(e.exception.status_code, 401)
        self.assertEqual(e.exception.detail, "Invalid token")

    def test_authenticate_user_valid(self):
        token = create_access_token(User(
            username='test_user',
            password='test_password'
        ))
        result = authenticate_user(token)
        self.assertIsNotNone(result)
    
    def test_authenticate_user_invalid(self):
        token = 'test_invalid_token'
        with self.assertRaises(HTTPException) as e:
            authenticate_user(token)
        self.assertEqual(e.exception.status_code, 401)
        self.assertEqual(e.exception.detail, "Invalid token")

    def test_get_user(self):
        db = MagicMock()
        db.query().filter().first.return_value = 'test_user'
        result = get_user(db, 'test_user')
        self.assertEqual(result, 'test_user')

    def test_get_user_none(self):
        db = MagicMock()
        db.query().filter().first.return_value = None
        result = get_user(db, 'test_user')
        self.assertEqual(result, None)

    def test_get_user_empty(self):
        db = MagicMock()
        db.query().filter().first.return_value = None
        result = get_user(db, '')
        self.assertEqual(result, None)