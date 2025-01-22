from fastapi import APIRouter, HTTPException
from src.auth import service as auth_service
from src.models.user import UserModelCreation
from src.users.service import authenticate_user

auth_router = APIRouter()

@auth_router.post("/login", tags=["auth"])
def login(credentials: UserModelCreation):
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"token": auth_service.create_access_token(user)}