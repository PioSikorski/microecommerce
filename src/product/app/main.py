import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.product.app.api.router import router
from src.core.config import TEST
from src.product.app.api.service import product_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if not TEST:
            product_consumer.start()
        yield
    finally:
        if not TEST:
            product_consumer.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(router)