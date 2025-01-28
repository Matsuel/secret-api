from fastapi import APIRouter
from fastapi import HTTPException, status
from pydantic import BaseModel
from .service import get_spaces_list
from .service import get_space
from .service import create_space
from .service import update_space
from .service import invite_user_to_space
from .service import delete_space
from .service import accept_invitation
from fastapi import Depends
from ..auth.service import get_current_user
from src.models.results import PostModelResponse, PutModelResponse, DeleteModelResponse, SpaceModel


class SpaceCreateRequest(BaseModel):
    name: str
    is_public: bool

class SpaceUpdateRequest(BaseModel):
    name: str
    is_public: bool

spaces_router = APIRouter()

@spaces_router.get("/spaces", tags=["spaces"], response_model=list[SpaceModel], status_code=200)
def getSpacesList():
    # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de retourner les spaces
    spaces = get_spaces_list()
    return spaces


@spaces_router.get("/space/{space_id}", tags=["spaces"], response_model=SpaceModel, status_code=200)
def getSpace(space_id: int):
    # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de retourner les informations
    space = get_space(space_id)
    if not space:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Space not found")
    return space

@spaces_router.post("/space", tags=["spaces"], status_code=201, response_model=PostModelResponse)
def createSpace(space: SpaceCreateRequest):
        # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de créer un space avec l'id de l'utilisateur comme propriétaire
        new_space = create_space(space.name, space.is_public)
        if not new_space:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Space could not be created")
        return {"message": "Space created successfully"}

@spaces_router.put("/space/{space_id}", tags=["spaces"], status_code=200, response_model=PutModelResponse)
def updateSpace(space_id: int, space: SpaceUpdateRequest):
        # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de mettre à jour les informations si l'utilisateur est le propriétaire du space
        updated_space = update_space(space_id, space.name, space.is_public)
        if not updated_space:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Space not found")
        return {"message": "Space updated successfully"}

@spaces_router.put("/space/{space_id}/invite/{user_id}", tags=["spaces"])
def inviteUserInSpace(space_id: int, user_id: int):
    try:
        invite_user_to_space(space_id, user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "User invited successfully"}

@spaces_router.put("/space/{space_id}/invite/accepted", tags=["spaces"])
def acceptInvitation(space_id: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("user_id")
    
    accept_invitation(space_id, user_id)
    
    return {"message": "Invitation accepted"}

@spaces_router.delete("/space/{space_id}", tags=["spaces"], status_code=200, response_model=DeleteModelResponse)
def deleteSpace(space_id: int):
    # Prendre un token en paramètre et vérifier si l'utilisateur est authentifié avant de supprimer si l'utilisateur est le propriétaire du space
     deleteSpace = delete_space(space_id)
     if not deleteSpace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Space not found")
     return {"message": "Space deleted successfully"}