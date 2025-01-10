from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    followsCount = Column(Integer, nullable=False, default=0)
    followersCount = Column(Integer, nullable=False, default=0)

     # Relation avec Secret
    secrets = relationship("Secret", back_populates="user")
    
class UserModelCreation(BaseModel):
    username: str
    password: str
    
class UserModel(BaseModel):
    id: int
    username: str
    followsCount: int
    followersCount: int
