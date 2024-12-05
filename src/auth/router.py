from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.post("/user/auth", tags=["auth"])
def authenticate_user():
    pass