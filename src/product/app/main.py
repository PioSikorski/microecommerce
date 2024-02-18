from contextlib import asynccontextmanager
from threading import Thread

from fastapi import FastAPI

from src.product.app.api.router import router
from src.product.app.api.service import start_product_rabbit


@asynccontextmanager
async def lifespan(app: FastAPI):
    product_rpc_thread = Thread(target=start_product_rabbit)
    product_rpc_thread.start()
    yield
    product_rpc_thread.join()


app = FastAPI(lifespan=lifespan)

app.include_router(router)