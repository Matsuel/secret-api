from sqlalchemy.orm import Session
from src.users.service import get_user_by_id
from src.models.user import User
import jwt
from datetime import datetime

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_access_token(user: User) -> dict:
    from datetime import timedelta
    payload = {"user_id": user.id, "exp": datetime.now() + timedelta(seconds=900)}
    return jwt.encode(payload, "secret", algorithm="HS256")

def verify_token(token: str) -> dict|None:
    try:
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        return data
    except:
        return None

def authenticate_user(token: str):
    data = verify_token(token)
    if not data:
        return False
    user = get_user_by_id(data['user_id'])
    if not user:
        return False
    return user