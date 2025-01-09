from fastapi import FastAPI
from src.users.router import users_router
from src.spaces.router import spaces_router
from src.sekrets.router import sekrets_router
from src.auth.router import auth_router
from src.docs.router import docs_router
from src.followers.router import followers_router
from src.models.database import init_db

init_db()

app = FastAPI(
    title="Sekret API",
)


app.include_router(users_router)
app.include_router(followers_router)
app.include_router(spaces_router)
app.include_router(sekrets_router)
app.include_router(auth_router)
app.include_router(docs_router)
