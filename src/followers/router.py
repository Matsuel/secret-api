from fastapi import APIRouter, Depends
from src.auth import service as auth_service
from fastapi import HTTPException
from src.followers.service import follow_user_in_db, get_followers_in_db, get_follows_in_db

followers_router = APIRouter()

# Get all follows of a user
@followers_router.get("/user/{user_id}/follow", tags=["users"])
def get_user_follows(user_id: int, current_user: dict = Depends(auth_service.get_current_user), offset: int = 0, limit: int = 100):
    follows = get_follows_in_db(user_id, offset, limit)
    if not follows:
        raise HTTPException(status_code=404, detail="No follows found")
    return follows

# Get all followers of a user
@followers_router.get("/user/{user_id}/followers", tags=["users"])
def get_user_followers(user_id: int, current_user: dict = Depends(auth_service.get_current_user), offset: int = 0, limit: int = 100):
    followers = get_followers_in_db(user_id, offset, limit)
    if not followers:
        raise HTTPException(status_code=404, detail="No followers found")
    return followers

@followers_router.post("/user/follow/{user_to_follow_id}", tags=["users"])
def follow_user(user_to_follow_id: int, current_user: dict = Depends(auth_service.get_current_user)):
    result = follow_user_in_db(current_user.get('id'), user_to_follow_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User cannot follow himself or user not found")
    if result:
        return {"message": "User followed"}
    else:
        return {"message": "User unfollowed"}
