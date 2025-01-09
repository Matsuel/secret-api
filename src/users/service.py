from ..models.user import User
from src.models.database import SessionLocal
from fastapi import HTTPException


def get_users_list():
    with SessionLocal() as session:
        users = session.query(User).all()
        if not users:
            return []
        return users
    
def get_user_by_id(user_id: int):
    with SessionLocal() as session:
        user = session.query(User).get(user_id)
        return user