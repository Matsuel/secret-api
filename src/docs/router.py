from fastapi import APIRouter
from fastapi.responses import RedirectResponse

docs_router = APIRouter()

@docs_router.get("/", tags=["docs"])
def redirect_to_docs():
    return RedirectResponse(url="/docs")