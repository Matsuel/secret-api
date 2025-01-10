from fastapi import APIRouter
from fastapi import HTTPException, status
from pydantic import BaseModel
from .service import get_spaces_list
from .service import get_space
from .service import create_space
from .service import update_space
from .service import invite_user_to_space
from .service import delete_space
class SpaceCreateRequest(BaseModel):
    name: str
    is_public: bool

class SpaceUpdateRequest(BaseModel):
    name: str
    is_public: bool

spaces_router = APIRouter()

@spaces_router.get("/spaces", tags=["spaces"])
def getSpacesList():
    spaces = get_spaces_list()
    return spaces


@spaces_router.get("/space/{space_id}", tags=["spaces"])
def getSpace(space_id: int):
    space = get_space(space_id)
    return space

@spaces_router.post("/space", tags=["spaces"])
def createSpace(space: SpaceCreateRequest):
        print(f"Received: name={space.name}, is_public={space.is_public}")
        new_space = create_space(space.name, space.is_public)
        if not new_space:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Space could not be created")
        return {"message": "Space created successfully"}

@spaces_router.put("/space/{space_id}", tags=["spaces"])
def updateSpace(space_id: int, space: SpaceUpdateRequest):
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

@spaces_router.delete("/space/{space_id}", tags=["spaces"])
def deleteSpace(space_id: int):
     deleteSpace = delete_space(space_id)
     if not deleteSpace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Space not found")
     return {"message": "Space deleted successfully"}