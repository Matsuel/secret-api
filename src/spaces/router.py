from fastapi import APIRouter

spaces_router = APIRouter()

@spaces_router.post("/space", tags=["spaces"])
def create_space():
    pass

@spaces_router.put("/space/:space_id", tags=["spaces"])
def update_space(space_id: int):
    pass

@spaces_router.put("/space/:space_id/invite/:user_id", tags=["spaces"])
def invite_user(space_id: int, user_id: int):
    pass