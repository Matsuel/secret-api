from ..models.follower import Follower
from ..users.service import check_if_user_exists
from src.models.database import SessionLocal
from sqlalchemy import insert, delete

def is_following(user_id: int, followed_id: int):
    with SessionLocal() as session:
        follower = session.query(Follower).filter(Follower.user_id == user_id, Follower.follower_id == followed_id).first()
        return True if follower else False
    

def follow_user_in_db(user_id: int, followed_id: int):
    if not check_if_user_exists(user_id) or not check_if_user_exists(followed_id):
        return None
    if user_id == followed_id:
        return None
    with SessionLocal() as session:
        result = True
        if is_following(user_id, followed_id):
            stmt = delete(Follower).where(Follower.user_id == user_id, Follower.follower_id == followed_id)
            result = False
        else:
            stmt = insert(Follower).values(user_id=user_id, follower_id=followed_id)
        session.execute(stmt)
        session.commit()
        return result
    
