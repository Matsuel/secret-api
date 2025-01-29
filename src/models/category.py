from sqlalchemy import Column, Integer, String
from .database import Base
from pydantic import BaseModel

class Category(Base):
    # TODO: user_id should be a foreign key to the users table
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    
class CategoryModel(BaseModel):
    # TODO: user_id should be a foreign key to the users table
    id: int
    name: str
    
class CategoryEdit(BaseModel):
    name: str
