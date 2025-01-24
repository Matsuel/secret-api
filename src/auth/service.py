from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from src.users.service import get_user_by_id
from src.models.user import User
import jwt
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "your_secret_key"  # Mets une vraie clé ici ou utilise une variable d'environnement
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_access_token(user: User) -> dict:
    from datetime import timedelta
    payload = {"user_id": user.id, "exp": datetime.now() + timedelta(seconds=900)}
    return jwt.encode(payload, "your_secret_key", algorithm="HS256")

def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def authenticate_user(token: str):
    data = verify_token(token)
    if not data:
        return False
    user = get_user_by_id(data['user_id'])
    if not user:
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = verify_token(token)
    user = get_user_by_id(payload['user_id'])
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return user