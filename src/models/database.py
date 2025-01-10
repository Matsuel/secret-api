from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration de la base de données
DATABASE_URL = "postgresql://forantis:password@localhost:5432/sekret"

# Créer l'engine
engine = create_engine(DATABASE_URL)

# Créer la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Définir Base une seule fois
Base = declarative_base()

# Créer les tables au démarrage
def init_db():
    from .user import User
    from .category import Category
    from .follower import Follower
    from .liked_secret import LikedSecret
    from .secret import Secret
    from .shared_space_user import SharedSpaceUser
    from .shared_space import SharedSpace
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()