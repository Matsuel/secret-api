from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class SharedSpace(Base):
    __tablename__ = 'shared_spaces'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False, default=False)