from fastapi import FastAPI

from src.cart.app.api import router


app = FastAPI()

app.include_router(router.router)
