from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Secret(Base):
    __tablename__ = 'secrets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    is_public = Column(Boolean, nullable=False)
    shares_spaces_id = Column(Integer, nullable=True)
    anonymous = Column(Boolean, nullable=False)