from fastapi import FastAPI

from src.order.app.api import router


app = FastAPI()

app.include_router(router.router)
