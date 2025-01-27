import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    api_key_id = Column(String, nullable=False)
    followsCount = Column(Integer, nullable=False)
    followersCount = Column(Integer, nullable=False)
    password = Column(String, nullable=False)

class Secret(Base):
    __tablename__ = 'secrets'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    is_public = Column(Boolean, nullable=False)
    shared_space_id = Column(Integer, ForeignKey('shared_spaces.id'), nullable=False)
    anonymous = Column(Boolean, nullable=False)
    likesCount = Column(Integer, nullable=False)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class SharedSpace(Base):
    __tablename__ = 'shared_spaces'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False)

class SharedSpaceUser(Base):
    __tablename__ = 'shared_space_users'
    id = Column(Integer, primary_key=True)
    shared_space_id = Column(Integer, ForeignKey('shared_spaces.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    invitation_accepted = Column(Boolean, nullable=False)

class LikedSecret(Base):
    __tablename__ = 'liked_secrets'
    id = Column(Integer, primary_key=True)
    secret_id = Column(Integer, ForeignKey('secrets.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class Follower(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)

# an Engine, which the Session will use for connection
# resources, typically in module scope
engine = create_engine("postgresql+psycopg2://forantis:password@localhost:5432/sekret")

# Create all tables
Base.metadata.create_all(engine)

# a sessionmaker(), also in the same scope as the engine
Session = sessionmaker(engine)

# we can now construct a Session() without needing to pass the
# engine each time
with Session() as session:
    session.execute(
    insert(Category),
    [
        {"id": 1, "name": "Work"},
        {"id": 2, "name": "Personal"},
        {"id": 3, "name": "Hobbies"},
        {"id": 4, "name": "Travel"},
        {"id": 5, "name": "Food"},
    ],
    )
    session.execute(
    insert(SharedSpace),
    [
        {"id": 1, "name": "Public", "is_public": True},
        {"id": 2, "name": "Friends", "is_public": False},
        {"id": 3, "name": "Family", "is_public": False},
    ],
    )
    session.execute(
        insert(User),
     [
        {"id": 1, "username": "spongebob", "api_key_id": "1234", "followsCount": 10, "followersCount": 15, "password": "password1"},
        {"id": 2, "username": "patrick", "api_key_id": "1235", "followsCount": 15, "followersCount": 10, "password": "password2"},
        {"id": 3, "username": "squidward", "api_key_id": "1236", "followsCount": 5, "followersCount": 5, "password": "password3"},
        {"id": 4, "username": "sandy", "api_key_id": "1237", "followsCount": 5, "followersCount": 5, "password": "password4"},
        {"id": 5, "username": "mrkrabs", "api_key_id": "1238", "followsCount": 5, "followersCount": 5, "password": "password5"},
        {"id": 6, "username": "plankton", "api_key_id": "1239", "followsCount": 5, "followersCount": 5, "password": "password6"},
        {"id": 7, "username": "gary", "api_key_id": "1240", "followsCount": 5, "followersCount": 5, "password": "password7"},
        {"id": 8, "username": "pearl", "api_key_id": "1241", "followsCount": 5, "followersCount": 5, "password": "password8"},
        {"id": 9, "username": "mrsPuff", "api_key_id": "1242", "followsCount": 5, "followersCount": 5, "password": "password9"},
        {"id": 10, "username": "larry", "api_key_id": "1243", "followsCount": 5, "followersCount": 5, "password": "password10"},
        {"id": 11, "username": "squilliam", "api_key_id": "1244", "followsCount": 5, "followersCount": 5, "password": "password11"},
     ],
    )
    session.execute(
        insert(Secret),
    [
        {"id": 1, "text": "I love my job", "user_id": 1, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 10},
        {"id": 2, "text": "I hate my job", "user_id": 2, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 10},
        {"id": 3, "text": "I'm a great cook", "user_id": 3, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 10},
        {"id": 4, "text": "I'm a terrible cook", "user_id": 4, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 10},
        {"id": 5, "text": "I'm a great cook", "user_id": 5, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 10},
        {"id": 6, "text": "I'm a terrible cook", "user_id": 6, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 10},
        {"id": 7, "text": "I'm a great cook", "user_id": 7, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 10},
        {"id": 8, "text": "I'm a terrible cook", "user_id": 8, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 10},
        {"id": 9, "text": "I'm a great cook", "user_id": 9, "category_id": 1, "is_public": True, "shared_space_id": 1, "anonymous": False, "likesCount": 10},
    ],
    )
    session.execute(
    insert(SharedSpaceUser),
    [
        {"id": 1, "shared_space_id": 1, "user_id": 1, "invitation_accepted": True},
        {"id": 2, "shared_space_id": 1, "user_id": 2, "invitation_accepted": True},
        {"id": 3, "shared_space_id": 1, "user_id": 3, "invitation_accepted": True},
        {"id": 4, "shared_space_id": 1, "user_id": 4, "invitation_accepted": True},
        {"id": 5, "shared_space_id": 1, "user_id": 5, "invitation_accepted": True},
        {"id": 6, "shared_space_id": 1, "user_id": 6, "invitation_accepted": True},
        {"id": 7, "shared_space_id": 1, "user_id": 7, "invitation_accepted": True},
        {"id": 8, "shared_space_id": 1, "user_id": 8, "invitation_accepted": True},
        {"id": 9, "shared_space_id": 1, "user_id": 9, "invitation_accepted": True},
    ],
    )
    session.execute(
    insert(LikedSecret),
    [
        {"id": 1, "secret_id": 1, "user_id": 2},
        {"id": 2, "secret_id": 1, "user_id": 3},
        {"id": 3, "secret_id": 1, "user_id": 4},
        {"id": 4, "secret_id": 1, "user_id": 5},
        {"id": 5, "secret_id": 1, "user_id": 6},
        {"id": 6, "secret_id": 1, "user_id": 7},
        {"id": 7, "secret_id": 1, "user_id": 8},
    ],
    )
    session.execute(
    insert(Follower),
    [
        {"id": 1, "user_id": 1, "follower_id": 2},
        {"id": 2, "user_id": 1, "follower_id": 3},
        {"id": 3, "user_id": 1, "follower_id": 4},
        {"id": 4, "user_id": 1, "follower_id": 5},
        {"id": 5, "user_id": 1, "follower_id": 6},
        {"id": 6, "user_id": 1, "follower_id": 7},
        {"id": 7, "user_id": 1, "follower_id": 8},
        {"id": 8, "user_id": 1, "follower_id": 9},
        {"id": 9, "user_id": 1, "follower_id": 10},
        {"id": 10, "user_id": 1, "follower_id": 11},
    ],
    )

    session.commit()