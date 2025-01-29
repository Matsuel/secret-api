from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from src.auth import service as auth_service
from src.models.database import get_db
from src.users.service import authenticate_user
from src.models.user import UserModelCreation
from src.users.service import create_user_in_db
from src.models.results import LoginModelResponse, PostModelResponse

auth_router = APIRouter()

@auth_router.post("/auth/login", tags=["auth"])
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):    
    # Authentifie l'utilisateur
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Crée un token d'accès
    token = auth_service.create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}

@auth_router.post("/auth/register", tags=["auth"], status_code=201, response_model=PostModelResponse)
def create_user(user: UserModelCreation):
    result = create_user_in_db(user)
    if result is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created"}