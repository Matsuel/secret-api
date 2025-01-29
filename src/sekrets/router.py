from fastapi import APIRouter, HTTPException, Depends, status
from src.models.secret import Secret, CreateSecret, UpdateSecret
from src.models.database import SessionLocal
from src.models.database import SessionLocal
from src.auth import service as auth_service
from src.sekrets.service import create_secret_db, get_all_secrets_from_db, get_secret_by_id, get_secrets_by_space_id, update_secret_in_db, delete_secret_in_db, like_secret_in_db
from src.models.results import PostModelResponse, PutModelResponse, DeleteModelResponse, SecretModel


sekrets_router = APIRouter()

##############################
# POST - Create a new secret

@sekrets_router.post("/secret", tags=["secrets"], status_code=status.HTTP_201_CREATED, response_model=PostModelResponse)
def create_secret(secret: CreateSecret, current_user: dict = Depends(auth_service.get_current_user)):
    result = create_secret_db(secret, current_user.get('id'))

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating secret")
    
    if result == "Utilisateur non trouvé":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    
    if result == "Catégorie non trouvé":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Catégorie non trouvé")
    
    return {"message": "Secret created successfully"}

######################
# Get all secrets

@sekrets_router.get("/secrets", tags=["secrets"], status_code=status.HTTP_200_OK, response_model=list[SecretModel])
def get_secrets_all(offset: int = 0, limit: int = 100, current_user: dict = Depends(auth_service.get_current_user)):
    result = get_all_secrets_from_db(offset, limit)
    return result

#############################
# Get a secret by secret_id

@sekrets_router.get("/secret/{secret_id}", tags=["secrets"], status_code=status.HTTP_200_OK, response_model=SecretModel)
def get_secret_id(secret_id: int, current_user: dict = Depends(auth_service.get_current_user)):
    # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de retourner les informations, et vérifier si l'utilisateur a le droit de voir le secret
    result = get_secret_by_id(secret_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")
    return result

################################
# Get secret by space_id

@sekrets_router.get("/secret/space/{space_id}", tags=["secrets"], status_code=status.HTTP_200_OK)
def get_secrets(space_id: int, current_user: dict = Depends(auth_service.get_current_user)):
    result = get_secrets_by_space_id(space_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")
    return result

################################
# Update a secret by secret_id

@sekrets_router.put("/secret/{secret_id}", tags=["secrets"], status_code=status.HTTP_200_OK, response_model=PutModelResponse)
def update_secret_content(secret_id: int, secret: UpdateSecret, current_user: dict = Depends(auth_service.get_current_user)):
    result = update_secret_in_db(secret_id, secret)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")
    return {"message": "Secret updated successfully", "data": secret}

#########################
# Delete a secret by id

@sekrets_router.delete("/secret/{secret_id}", tags=["secrets"], status_code=status.HTTP_200_OK, response_model=DeleteModelResponse)
def delete_secret(secret_id: int, current_user: dict = Depends(auth_service.get_current_user)):
    result = delete_secret_in_db(secret_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")
    return {"message": "Secret deleted successfully"}

################################
# Like a secret by secret_id

@sekrets_router.post("/secret/{secret_id}/like", tags=["secrets"], status_code=status.HTTP_200_OK, response_model=PostModelResponse)
def like_secret(secret_id: int, current_user: dict = Depends(auth_service.get_current_user)):
    result = like_secret_in_db(secret_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")
    return {"message": "Secret liked successfully"}

@sekrets_router.get("/secrets/popular", tags=["secrets"], status_code=status.HTTP_200_OK, response_model=list[SecretModel])
def get_popular_secrets(offset: int = 0, limit: int = 10, current_user: dict = Depends(auth_service.get_current_user)):
    with SessionLocal() as session:
        stmt = session.query(Secret).order_by(Secret.likesCount.desc()).offset(offset).limit(limit).all()
    return stmt