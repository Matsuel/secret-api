from fastapi import APIRouter

secrets_router = APIRouter()

@secrets_router.post("/secret", tags=["secrets"])
def create_secret():
    pass

@secrets_router.put("/secret/:secret_id", tags=["secrets"])
def update_secret_content(secret_id: int):
    pass

@secrets_router.delete("/secret/:secret_id", tags=["secrets"])
def delete_secret(secret_id: int):
    pass

@secrets_router.post("/secret/:secret_id/like", tags=["secrets"])
def like_secret(secret_id: int):
    pass