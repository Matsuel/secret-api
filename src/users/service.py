from ..models.user import User
from src.models.database import SessionLocal
from sqlalchemy import insert


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

def check_if_user_exists(user_id: int):
    with SessionLocal() as session:
        user = session.query(User).get(user_id)
        if user is None:
            return False
        return True
    
def check_username_exists(username: str):
    with SessionLocal() as session:
        user = session.query(User).filter(User.username == username).first()
        if user is None:
            return False
        return True
    
def create_user_in_db(user: User):
    if check_username_exists(user.username):
        return None
    with SessionLocal() as session:
        stmt = insert(User).values(username=user.username, password=user.password)
        session.execute(stmt)
        session.commit()
        return user