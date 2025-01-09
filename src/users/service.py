from ..models.user import User
from src.models.database import SessionLocal


def get_users_list():
    with SessionLocal() as session:
        users = session.query(User).all()
        if not users:
            return []
        return users