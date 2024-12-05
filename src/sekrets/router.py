from fastapi import APIRouter

sekrets_router = APIRouter()

@sekrets_router.post("/secret", tags=["secrets"])
def create_secret():
    pass

@sekrets_router.get("/secrets/:space_id", tags=["secrets"])
def get_secrets(space_id: int):
    pass

@sekrets_router.put("/secret/:secret_id", tags=["secrets"])
def update_secret_content(secret_id: int):
    pass

@sekrets_router.delete("/secret/:secret_id", tags=["secrets"])
def delete_secret(secret_id: int):
    pass

@sekrets_router.post("/secret/:secret_id/like", tags=["secrets"])
def like_secret(secret_id: int):
    pass