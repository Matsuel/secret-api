from fastapi import FastAPI
from src.users.router import users_router
from src.spaces.router import spaces_router
from src.sekrets.router import sekrets_router
from src.auth.router import auth_router
from src.followers.router import followers_router
from src.models.database import init_db

init_db()

description = """
Documentation du projet Sekret API
Ce projet est une API pour une application de type réseau social.
Elle permet de créer des utilisateurs, de créer des espaces, de créer des sekrets et de suivre d'autres utilisateurs.
"""


app = FastAPI(
    title="Sekret API",
    description=description,
    version="1.0",
    docs_url="/",
)


app.include_router(users_router)
app.include_router(followers_router)
app.include_router(spaces_router)
app.include_router(sekrets_router)
app.include_router(auth_router)
