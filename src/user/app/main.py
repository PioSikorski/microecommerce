from contextlib import asynccontextmanager
from threading import Thread

from fastapi import FastAPI

from src.user.app.api import login, user
from src.user.app.api.service import start_user_rabbit

@asynccontextmanager
async def lifespan(app: FastAPI):
    user_rpc_thread = Thread(target=start_user_rabbit)
    user_rpc_thread.start()
    yield
    user_rpc_thread.join()
    

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(login.router)