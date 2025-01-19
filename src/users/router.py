from fastapi import APIRouter
from .service import get_users_list, get_user_by_id, create_user_in_db, delete_user_in_db, update_user_in_db
from src.sekrets.service import get_secrets_by_user_id
from fastapi import HTTPException
from src.models.user import UserModelCreation, UserModel

users_router = APIRouter()

@users_router.get("/users", tags=["users"])
def get_users(offset: int = 0, limit: int = 10):
    users = get_users_list(offset, limit)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@users_router.get("/user/{user_id}", tags=["users"])
def get_user_infos(user_id: int):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    secrets = get_secrets_by_user_id(user_id)
    # TODO: Créer une fonction pour formater les données
    user["followers"] = f"/user/{user_id}/followers"
    user["follows"] = f"/user/{user_id}/follows"
    user["secrets"] = secrets
    return user

@users_router.post("/user", tags=["users"], status_code=201)
def create_user(user: UserModelCreation):
    result = create_user_in_db(user)
    if result is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created"}

@users_router.put("/user/{user_id}", tags=["users"], status_code=200)
def update_user(user_id: int, user: UserModelCreation):
    result = update_user_in_db(user_id, user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found or username already exists")
    return {"message": "User updated"}

@users_router.delete("/user/{user_id}", tags=["users"], status_code=200)
def delete_user(user_id: int):
    result = delete_user_in_db(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}