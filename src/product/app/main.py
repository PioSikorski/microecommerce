from fastapi import FastAPI
from src.product.app.api.router import router

app = FastAPI()

app.include_router(router)