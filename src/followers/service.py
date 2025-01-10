from src.models.follower import Follower
from src.models.user import User
from src.users.service import check_if_user_exists, get_user_by_id
from src.models.database import SessionLocal
from sqlalchemy import insert, delete, update

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
            edit_followers_count(followed_id, False)
            edit_follows_count(user_id, False)
            result = False
        else:
            stmt = insert(Follower).values(user_id=user_id, follower_id=followed_id)
            edit_followers_count(followed_id, True)
            edit_follows_count(user_id, True)
        session.execute(stmt)
        session.commit()
        return result
    
def get_follows_in_db(user_id: int, offset: int = 0, limit: int = 100):
    with SessionLocal() as session:
        follows = session.query(Follower.follower_id).filter(Follower.user_id == user_id).offset(offset).limit(limit).all()
        follows = [follow.follower_id for follow in follows]
        followers_infos = []
        for follow in follows:
            followers_infos.append(get_user_by_id(follow))
        return followers_infos
    
def get_followers_in_db(user_id: int, offset: int = 0, limit: int = 100):
    with SessionLocal() as session:
        followers = session.query(Follower.user_id).filter(Follower.follower_id == user_id).offset(offset).limit(limit).all()
        followers = [follower.user_id for follower in followers]
        followers_infos = []
        for follower in followers:
            followers_infos.append(get_user_by_id(follower))
        return followers_infos
    
def edit_followers_count(user_id: int, increment: bool):
    with SessionLocal() as session:
        stmt = update(User).where(User.id == user_id)
        if increment:
            stmt = stmt.values(followersCount=User.followersCount + 1)
        else:
            stmt = stmt.values(followersCount=User.followersCount - 1)
        session.execute(stmt)
        session.commit()
        
def edit_follows_count(user_id: int, increment: bool):
    with SessionLocal() as session:
        stmt = update(User).where(User.id == user_id)
        if increment:
            stmt = stmt.values(followsCount=User.followsCount + 1)
        else:
            stmt = stmt.values(followsCount=User.followsCount - 1)
        session.execute(stmt)
        session.commit()