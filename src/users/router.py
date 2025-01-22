from fastapi import APIRouter
from fastapi import HTTPException
from src.models.user import UserModelCreation
from src.auth.service import authenticate_user
from src.users.service import get_users_list, create_user_in_db, delete_user_in_db, update_user_in_db, get_user_by_id

users_router = APIRouter()

@users_router.get("/users", tags=["users"])
def get_users(offset: int = 0, limit: int = 10, token: str = None):
    if not authenticate_user(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    users = get_users_list(offset, limit)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@users_router.get("/user/{user_id}", tags=["users"])
def get_user_infos(user_id: int, token: str = None):
    if not authenticate_user(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.post("/user", tags=["users"], status_code=201)
def create_user(user: UserModelCreation):
    result = create_user_in_db(user)
    if result is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created"}

@users_router.put("/user/", tags=["users"], status_code=200)
def update_user(user: UserModelCreation, token: str = None):
    authenticated_user = authenticate_user(token)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = update_user_in_db(authenticated_user['id'], user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found or username already exists")
    return {"message": "User updated"}

@users_router.delete("/user/", tags=["users"], status_code=200)
def delete_user(token: str = None):
    authenticated_user = authenticate_user(token)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = delete_user_in_db(authenticated_user['id'])
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}