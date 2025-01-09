from fastapi import APIRouter
from .service import get_users_list

users_router = APIRouter()

@users_router.get("/users", tags=["users"])
def get_users():
    users = get_users_list()
    return users

@users_router.get("/user/{user_id}", tags=["users"])
def get_user_infos(user_id: int):
    print(user_id)
    pass

@users_router.post("/user", tags=["users"])
def create_user():
    pass

@users_router.put("/user/{user_id}", tags=["users"])
def update_user(user_id: int):
    pass

@users_router.delete("/user/{user_id}", tags=["users"])
def delete_user(user_id: int):
    pass

@users_router.get("/user/{user_id}/follow", tags=["users"])
def get_user_follows(user_id: int):
    pass

@users_router.get("/user/{user_id}/followers", tags=["users"])
def get_user_followers(user_id: int):
    pass