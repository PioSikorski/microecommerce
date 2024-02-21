import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.user.app.api import login, user
from src.core.config import TEST
from src.user.app.api.service import user_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if not TEST:
            user_consumer.start()
        yield
    finally:
        if not TEST:
            user_consumer.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(login.router)