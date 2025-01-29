from src.models.database import Base, engine

def clean_db():
    # Supprimer toutes les tables
    Base.metadata.drop_all(bind=engine)
    # Recréer les tables
    Base.metadata.create_all(bind=engine)
    print("La base de données a été nettoyée avec succès.")

if __name__ == "__main__":
    clean_db()