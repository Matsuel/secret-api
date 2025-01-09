from sqlalchemy import Column, Integer
from .database import Base

class Follower(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    follower_id = Column(Integer, nullable=False)