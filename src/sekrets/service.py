from src.models.user import User
from src.models.secret import Secret, CreateSecret
from src.models.database import SessionLocal
from sqlalchemy import insert, update

def create_secret_db(secret: CreateSecret, user_id: int):
    with SessionLocal() as session:

        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return "Utilisateur non trouvé"
        
        stmt = insert(Secret).values(
            text = secret.text,
            user_id = user.id,
            category_id = secret.category_id,
            is_public = secret.is_public,
            shared_space_id = secret.shared_space_id,
            anonymous = secret.anonymous,
            likesCount = secret.likesCount
        )
        session.execute(stmt)
        session.commit()
    return True

def get_secret_by_id(secret_id: int):
    with SessionLocal() as session:
        space = session.query(Secret).filter(Secret.id == secret_id).first()
        return space if space else None

def get_all_secrets_from_db(offset: int = 0, limit: int = 100):
    with SessionLocal() as session:
        secrets = session.query(Secret).offset(offset).limit(limit).all()
    return secrets if secrets else None

def get_secrets_by_space_id(space_id: int):
    with SessionLocal() as session:
        stmt = session.query(Secret).filter(Secret.shared_space_id == space_id).first()
    return stmt

def get_secrets_by_user_id(user_id: int):
    with SessionLocal() as session:
        stmt = session.query(Secret).filter(Secret.user_id == user_id).all()
    return stmt

def update_secret_in_db(secret_id: int, secret: Secret):
    if not get_secret_by_id(secret_id):
        return False
    with SessionLocal() as session:
        stmt = (
            update(Secret)
            .where(Secret.id == secret_id)
            .values(
                text=secret.text,
                is_public=secret.is_public,
                anonymous=secret.anonymous,
                category_id=secret.category_id,
                shared_space_id=secret.shared_space_id
            )
        )
        session.execute(stmt)
        session.commit()
    return True

def delete_secret_in_db(secret_id: int):
    with SessionLocal() as session:
        stmt = session.query(Secret).filter(Secret.id == secret_id).first()
        session.delete(stmt)
        session.commit()
    return True

def like_secret_in_db(secret_id: int):
    with SessionLocal() as session:
        stmt = session.query(Secret).filter(Secret.id == secret_id).first()
        stmt.likesCount += 1
        session.commit()
    return True

