from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.auth import service as auth_service
from src.models.user import User
from src.auth.dependencies import oauth2_scheme

auth_router = APIRouter()

@auth_router.post("/login", tags=["auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.token, "token_type": "bearer"}

@auth_router.get("/users/me", tags=["auth"])
async def read_users_me(current_user: User = Depends(auth_service.get_current_active_user)):
    return current_user

@auth_router.get("/test-token", tags=["auth"])
async def test_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = auth_service.get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Token is valid", "user_id": user.id}