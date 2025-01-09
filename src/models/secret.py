from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Secret(Base):
    __tablename__ = 'secrets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    is_public = Column(Boolean, nullable=False)
    shared_space_id = Column(Integer, nullable=True)
    anonymous = Column(Boolean, nullable=False)
    likesCount = Column(Integer, nullable=False, default=0)