from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Secret(Base):
    __tablename__ = 'secrets'

    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )

    text = Column(
        String,
        nullable=False
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    category_id = Column(
        Integer,
        nullable=False
    )

    is_public = Column(
        Boolean,
        nullable=False
    )

    shared_space_id = Column(
        Integer,
        nullable=True
    )

    anonymous = Column(
        Boolean, 
        nullable=False
    )

    likesCount = Column(
        Integer, 
        nullable=False, 
        default=0
    )

class CreateSecret(BaseModel):
    text: str
    user_id: int
    category_id: int
    is_public: bool
    shared_space_id: int
    anonymous: bool
    likesCount: int

class UpdateSecret(BaseModel):
    text: str
    is_public: bool
    anonymous: bool
    category_id: int
    shared_space_id: int