from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SharedSpaceUser(Base):
    __tablename__ = 'shared_spaces_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    shared_space_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    invitation_accepted = Column(Boolean, nullable=False, default=False)