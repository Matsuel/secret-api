from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LikedSecret(Base):
    __tablename__ = 'liked_secrets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    secret_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)