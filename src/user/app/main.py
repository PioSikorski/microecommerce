from fastapi import FastAPI

from src.user.app.api import login, user

app = FastAPI()

app.include_router(user.router)
app.include_router(login.router)
