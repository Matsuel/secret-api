from fastapi import APIRouter
from fastapi import HTTPException
from src.followers.service import follow_user_in_db, get_followers_in_db, get_follows_in_db
from src.auth.service import authenticate_user

followers_router = APIRouter()

@followers_router.get("/user/{user_id}/follow", tags=["users"])
def get_user_follows(user_id: int, token: str, offset: int = 0, limit: int = 100):
    if not authenticate_user(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    follows = get_follows_in_db(user_id, offset, limit)
    if not follows:
        raise HTTPException(status_code=404, detail="No follows found")
    return follows

@followers_router.get("/user/{user_id}/followers", tags=["users"])
def get_user_followers(user_id: int, token: str, offset: int = 0, limit: int = 100):
    if not authenticate_user(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    followers = get_followers_in_db(user_id, offset, limit)
    if not followers:
        raise HTTPException(status_code=404, detail="No followers found")
    return followers

@followers_router.post("/user/follow/{user_to_follow_id}", tags=["users"])
def follow_user(token: str, user_to_follow_id: int):
    authenticated_user = authenticate_user(token)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = follow_user_in_db(authenticated_user.get('id'), user_to_follow_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User cannot follow himself or user not found")
    if result:
        return {"message": "User followed"}
    else:
        return {"message": "User unfollowed"}
