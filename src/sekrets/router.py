from fastapi import APIRouter, HTTPException
from src.models.secret import Secret, CreateSecret, UpdateSecret
from src.models.database import SessionLocal
from src.models.database import SessionLocal
from src.sekrets.service import create_secret_db, get_all_secrets_from_db, get_secret_by_id, get_secrets_by_space_id, update_secret_in_db, delete_secret_in_db, like_secret_in_db
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

@sekrets_router.get("/secrets", tags=["secrets"], status_code=200)
def get_secrets_all(offset: int = 0, limit: int = 100):
    result = get_all_secrets_from_db(offset, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No secrets found")
    return result

#############################
# Get a secret by secret_id

@sekrets_router.get("/secret/{secret_id}", tags=["secrets"], status_code=200)
def get_secret_id(secret_id: int):
    result = get_secret_by_id(secret_id)
    if not result:
        raise HTTPException(status_code=404, detail="Secret not found")
    return result

################################
# Get secret by space_id

@sekrets_router.get("/secret/space/{space_id}", tags=["secrets"], status_code=200)
def get_secrets(space_id: int):
    result = get_secrets_by_space_id(space_id)
    if not result:
        raise HTTPException(status_code=404, detail="Secret not found")
    return result

################################
# Update a secret by secret_id

@sekrets_router.put("/secret/{secret_id}", tags=["secrets"], status_code=200)
def update_secret_content(secret_id: int, secret: UpdateSecret):
    result = update_secret_in_db(secret_id, secret)
    if not result:
        raise HTTPException(status_code=404, detail="Secret not found")
    return {"message": "Secret updated successfully", "data": secret}

#########################
# Delete a secret by id

@sekrets_router.delete("/secret/{secret_id}", tags=["secrets"], status_code=200)
def delete_secret(secret_id: int):
    result = delete_secret_in_db(secret_id)
    if not result:
        raise HTTPException(status_code=404, detail="Secret not found")
    return {"message": "Secret deleted successfully"}

################################
# Like a secret by secret_id

@sekrets_router.post("/secret/{secret_id}/like", tags=["secrets"], status_code=200)
def like_secret(secret_id: int):
    result = like_secret_in_db(secret_id)
    if not result:
        raise HTTPException(status_code=404, detail="Secret not found")
    return {"message": "Secret liked successfully"}

@sekrets_router.get("/secrets/popular", tags=["secrets"], status_code=200)
def get_popular_secrets(offset: int = 0, limit: int = 10):
    with SessionLocal() as session:
        stmt = session.query(Secret).order_by(Secret.likesCount.desc()).offset(offset).limit(limit).all()
    return stmt