from fastapi import FastAPI
from users.router import users_router
from spaces.router import spaces_router
from sekrets.router import sekrets_router

app = FastAPI()


app.include_router(users_router)
app.include_router(spaces_router)
app.include_router(sekrets_router)