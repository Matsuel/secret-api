from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

# Configuration de la base de données

DATABASE_URL = f"postgresql://{getenv("DATABASE_USER")}:{getenv("DATABASE_PASSWORD")}@localhost:5432/{getenv("DATABASE_NAME")}"


# Créer l'engine
engine = create_engine(DATABASE_URL)

# Créer la session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Définir Base une seule fois
Base = declarative_base()

# Créer les tables au démarrage
def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()