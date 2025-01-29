from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base
from pydantic import BaseModel

class Category(Base):
    # TODO: user_id should be a foreign key to the users table
    __tablename__ = 'categories'
    
    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )

    name = Column(String, nullable=False)

    # Relation avec Secret
    secrets = relationship("Secret", back_populates="category")
    
class CategoryModel(BaseModel):
    # TODO: user_id should be a foreign key to the users table
    name: str
    
class CategoryEdit(BaseModel):
    name: str