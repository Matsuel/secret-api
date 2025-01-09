from sqlalchemy import Column, Integer, String
from .database import Base

class LikedSecret(Base):
    __tablename__ = 'liked_secrets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    secret_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)