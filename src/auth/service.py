from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.models.user import User
from src.users.service import verify_password
from src.auth.dependencies import oauth2_scheme
import hashlib

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def hash_username_to_token(username: str):
    return hashlib.sha256(username.encode()).hexdigest()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    if not user.token:
        user.token = hash_username_to_token(username)
        db.commit()
    return user

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user