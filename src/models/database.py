from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration de la base de données
DATABASE_URL = "postgresql://admin:admin@localhost:5432/sekret"

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
