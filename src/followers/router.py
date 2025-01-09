from fastapi import APIRouter
from fastapi import HTTPException
from src.followers.service import follow_user_in_db, get_followers_in_db, get_follows_in_db

followers_router = APIRouter()

@followers_router.get("/user/{user_id}/follow", tags=["users"])
def get_user_follows(user_id: int):
    follows = get_follows_in_db(user_id)
    return follows

@followers_router.get("/user/{user_id}/followers", tags=["users"])
def get_user_followers(user_id: int):
    followers = get_followers_in_db(user_id)
    return followers

@followers_router.post("/user/{user_id}/follow/{followed_id}", tags=["users"])
def follow_user(user_id: int, followed_id: int):
    result = follow_user_in_db(user_id, followed_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User cannot follow himself or user not found")
    if result:
        return {"message": "User followed"}
    else:
        return {"message": "User unfollowed"}
