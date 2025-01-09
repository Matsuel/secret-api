from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from ..models.user import User

DATABASE_URL = "postgresql://admin:admin@localhost:5432/sekret"

# Créer l'engine
engine = create_engine(DATABASE_URL)

# Créer la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ouvrir une session
session = SessionLocal()

def get_users_list():
    users = session.query(User).all()
    return users