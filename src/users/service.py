from src.models.user import User, UserModelCreation
from src.models.database import SessionLocal
from sqlalchemy import insert, update, delete
from src.sekrets.service import get_secrets_by_user_id
import bcrypt


def get_user_infos(user_id: int):
    with SessionLocal() as session:
        user = session.query(User.id, User.username, User.followsCount, User.followersCount).filter(User.id == user_id).first()
        if user is None:
            return None
        user = user._asdict()
        secrets = get_secrets_by_user_id(user_id)
        user["followers"] = f"/user/{user_id}/followers"
        user["follows"] = f"/user/{user_id}/follows"
        user["secrets"] = secrets
        return user


def get_users_list(offset: int = 0, limit: int = 10):
    with SessionLocal() as session:
        users = session.query(User.id, User.username, User.followsCount, User.followersCount).offset(offset).limit(limit).all()
        formated_users = []
        if not users:
            return []
        for user in users:
            formated_users.append(get_user_infos(user.id))
        return formated_users
    
def get_user_by_id(user_id: int):
    return get_user_infos(user_id)

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
    
def create_user_in_db(user: UserModelCreation):
    if check_username_exists(user.username):
        return None
    with SessionLocal() as session:
        stmt = insert(User).values(username=user.username, password=hash_password(user.password))
        session.execute(stmt)
        session.commit()
        return True
    
def delete_user_in_db(user_id: int):
    if not check_if_user_exists(user_id):
        return False
    with SessionLocal() as session:
        stmt = delete(User).where(User.id == user_id)
        session.execute(stmt)
        session.commit()
        return True
    
def update_user_in_db(user_id: int, user: User):
    if not check_if_user_exists(user_id):
        return False
    if user.username != "" and check_username_exists(user.username):
        return False
    with SessionLocal() as session:
        stmt = update(User).where(User.id == user_id)
        if user.username:
            stmt = stmt.values(username=user.username)
        if user.password:
            stmt = stmt.values(password=user.password)
        session.execute(stmt)
        session.commit()
        return True

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))