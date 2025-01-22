from fastapi import APIRouter
from fastapi import HTTPException
from src.followers.service import follow_user_in_db, get_followers_in_db, get_follows_in_db

followers_router = APIRouter()

@followers_router.get("/user/{user_id}/follow", tags=["users"])
def get_user_follows(user_id: int, offset: int = 0, limit: int = 100):
    # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de retourner les informations
    follows = get_follows_in_db(user_id, offset, limit)
    if not follows:
        raise HTTPException(status_code=404, detail="No follows found")
    return follows

@followers_router.get("/user/{user_id}/followers", tags=["users"])
def get_user_followers(user_id: int, offset: int = 0, limit: int = 100):
    # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de retourner les informations
    followers = get_followers_in_db(user_id, offset, limit)
    if not followers:
        raise HTTPException(status_code=404, detail="No followers found")
    return followers

@followers_router.post("/user/{user_id}/follow/{followed_id}", tags=["users"])
def follow_user(user_id: int, followed_id: int):
    # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de suivre un utilisateur, avec une vérification pour ne pas suivre soi-même, le user_id disparaitra dans le futur afin d'être récupéré depuis le token
    result = follow_user_in_db(user_id, followed_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User cannot follow himself or user not found")
    if result:
        return {"message": "User followed"}
    else:
        return {"message": "User unfollowed"}
