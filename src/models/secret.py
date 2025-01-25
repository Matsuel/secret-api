from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
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

    # Relation avec le modèle User
    user = relationship("User", back_populates="secrets")

    # Clé étrangère pour l'utilisateur
    user_id = Column(
        ForeignKey("users.id", ondelete="CASCADE"),
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