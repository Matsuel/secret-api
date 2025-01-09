from fastapi import APIRouter
from .service import get_users_list, get_user_by_id, create_user_in_db, delete_user_in_db, update_user_in_db
from fastapi import HTTPException
from src.models.user import UserModel

users_router = APIRouter()

@users_router.get("/users", tags=["users"])
def get_users():
    users = get_users_list()
    return users

@users_router.get("/user/{user_id}", tags=["users"])
def get_user_infos(user_id: int):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.post("/user", tags=["users"])
def create_user(user: UserModel):
    result = create_user_in_db(user)
    if result is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created"}

@users_router.put("/user/{user_id}", tags=["users"])
def update_user(user_id: int, user: UserModel):
    result = update_user_in_db(user_id, user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found or username already exists")
    return {"message": "User updated"}

@users_router.delete("/user/{user_id}", tags=["users"])
def delete_user(user_id: int):
    result = delete_user_in_db(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}