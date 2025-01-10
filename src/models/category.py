from sqlalchemy import Column, Integer, String
from .database import Base
from pydantic import BaseModel

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    
class CategoryModel(BaseModel):
    id: int
    name: str
    
class CategoryEdit(BaseModel):
    name: str