from ..models.user import User
from src.models.database import SessionLocal
from sqlalchemy import insert, update, delete


def get_users_list():
    with SessionLocal() as session:
        users = session.query(User.id, User.username, User.followsCount, User.followersCount).all()
        if not users:
            return []
        return [user._asdict() for user in users]
    
def get_user_by_id(user_id: int):
    with SessionLocal() as session:
        user = session.query(User.id, User.username, User.followsCount, User.followersCount).filter(User.id == user_id).first()
        return user._asdict() if user else None

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
    
def delete_user_in_db(user_id: int):
    if not check_if_user_exists(user_id):
        return False
    with SessionLocal() as session:
        stmt = delete(User).where(User.id == user_id)
        session.execute(stmt)
        session.commit()
        return True    