from fastapi import APIRouter, HTTPException
from sekrets.service import create_secret_db
from src.models.secret import Secret, CreateSecret, UpdateSecret
from src.models.database import SessionLocal
from src.models.database import SessionLocal
from sqlalchemy import insert
sekrets_router = APIRouter()

##############################
# POST - Create a new secret

@sekrets_router.post("/secret", tags=["secrets"])
def create_secret(secret: CreateSecret):
    result = create_secret_db(secret)

    if not result:
        raise HTTPException(status_code=400, detail="Error creating secret")
    
    if result == "Utilisateur non trouvé":
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    return {"message": "Secret created successfully"}

######################
# Get all secrets

@sekrets_router.get("/secrets", tags=["secrets"])
def get_secrets_all():
    with SessionLocal() as session:
        stmt = session.query(Secret).all()
    return stmt 

#############################
# Get a secret by secret_id

@sekrets_router.get("/secret/{secret_id}", tags=["secrets"])
def get_secret_id(secret_id: int):
    with SessionLocal() as session:
     stmt = session.query(Secret).filter(Secret.id == secret_id).first()
    return stmt

################################
# Get secret by space_id

@sekrets_router.get("/secret/space/{space_id}", tags=["secrets"])
def get_secrets(space_id: int):
    with SessionLocal() as session:
        stmt = session.query(Secret).filter(Secret.shared_space_id == space_id).first()
    return stmt

################################
# Update a secret by secret_id

@sekrets_router.put("/secret/{secret_id}", tags=["secrets"])
def update_secret_content(secret_id: int, secret: UpdateSecret):
    with SessionLocal() as session:
        stmt = session.query(Secret).filter(Secret.id == secret_id).first() 

        if secret.text is not None: 
            stmt.text = secret.text
        
        if secret.is_public is not None:
            stmt.is_public = secret.is_public
        if secret.anonymous is not None:
            stmt.anonymous = secret.anonymous
        
        if secret.category_id is not None:
            stmt.category_id = secret.category_id
        
        if secret.shared_space_id is not None:
            stmt.shared_space_id = secret.shared_space_id

        session.commit()

    return {"message": "Secret updated successfully", "data": secret}

#########################
# Delete a secret by id

@sekrets_router.delete("/secret/{secret_id}", tags=["secrets"])
def delete_secret(secret_id: int):
    with SessionLocal() as session:
        stmt = session.query(Secret).filter(Secret.id == secret_id).first()
        session.delete(stmt)
        session.commit()

    return {"message": "Secret deleted successfully"}

#! This route will delete all the secrets in the database
@sekrets_router.delete("/secrets", tags=["secrets"])
def delete_all_secret():
    with SessionLocal() as session:
        stmt = session.query(Secret).all()

        for secret in stmt:
            session.delete(secret)

        session.commit()

    return {"message": "All Secrets deleted successfully"}

################################
# Like a secret by secret_id

@sekrets_router.post("/secret/{secret_id}/like", tags=["secrets"])
def like_secret(secret_id: int):
    with SessionLocal() as session:
        stmt = session.query(Secret).filter(Secret.id == secret_id).first()
        stmt.likesCount += 1
        session.commit()

    return {"message": "Secret liked successfully"}