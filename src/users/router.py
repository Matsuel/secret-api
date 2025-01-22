from fastapi import APIRouter
from src.users.service import get_users_list, create_user_in_db, delete_user_in_db, update_user_in_db, get_user_by_id
from fastapi import HTTPException
from src.models.user import UserModelCreation

users_router = APIRouter()

@users_router.get("/users", tags=["users"])
def get_users(offset: int = 0, limit: int = 10):
    # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de retourner les informations
    users = get_users_list(offset, limit)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@users_router.get("/user/{user_id}", tags=["users"])
def get_user_infos(user_id: int):
    # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de retourner les informations
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

@users_router.put("/user/{user_id}", tags=["users"], status_code=200)
def update_user(user_id: int, user: UserModelCreation):
    # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de mettre à jour les informations
    result = update_user_in_db(user_id, user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found or username already exists")
    return {"message": "User updated"}

@users_router.delete("/user/{user_id}", tags=["users"], status_code=200)
def delete_user(user_id: int):
    # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de supprimer les informations, et vérifier si l'utilisateur a le droit de supprimer l'utilisateur il doit être le propriétaire de l'utilisateur
    result = delete_user_in_db(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}