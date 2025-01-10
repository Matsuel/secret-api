from sqlalchemy import Column, Integer, String
from .database import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    followsCount = Column(Integer, nullable=False, default=0)
    followersCount = Column(Integer, nullable=False, default=0)
    
class UserModelCreation(BaseModel):
    username: str
    password: str
    
class UserModel(BaseModel):
    id: int
    username: str
    followsCount: int
    followersCount: int