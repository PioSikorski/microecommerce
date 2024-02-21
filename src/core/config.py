import os
from typing import Any

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import EmailStr


load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = "aa7d737421b91a5cee8d014f68b0db13bb34034d833cbca5c064af23105250c7"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    FIRST_SUPERUSER: EmailStr = "admin@admin.com"
    FIRST_SUPERUSER_PASSWORD: str =  "admin"
    EMAIL_TEST_USER: EmailStr = "test@example.com"
    
    
settings = Settings()

TEST = os.getenv('TESTING', False)

USER_SERVICE = os.getenv('USER_SERVICE_NAME')
USER_POSTGRES_USER = os.getenv('USER_POSTGRES_USER')
USER_POSTGRES_PASSWORD = os.getenv('USER_POSTGRES_PASSWORD')
USER_POSTGRES_HOST = os.getenv('USER_POSTGRES_HOST')
USER_POSTGRES_PORT = os.getenv('USER_POSTGRES_PORT')
USER_POSTGRES_DB = os.getenv('USER_POSTGRES_DB')

PRODUCT_SERVICE = os.getenv('PRODUCT_SERVICE_NAME')
PRODUCT_POSTGRES_USER = os.getenv('PRODUCT_POSTGRES_USER')
PRODUCT_POSTGRES_PASSWORD = os.getenv('PRODUCT_POSTGRES_PASSWORD')
PRODUCT_POSTGRES_HOST = os.getenv('PRODUCT_POSTGRES_HOST')
PRODUCT_POSTGRES_PORT = os.getenv('PRODUCT_POSTGRES_PORT')
PRODUCT_POSTGRES_DB = os.getenv('PRODUCT_POSTGRES_DB')

ORDER_SERVICE = os.getenv('ORDER_SERVICE_NAME')
ORDER_MONGODB_USER = os.getenv('ORDER_MONGODB_USER')
ORDER_MONGODB_PASSWORD = os.getenv('ORDER_MONGODB_PASSWORD')
ORDER_MONGODB_HOST = os.getenv('ORDER_MONGODB_HOST')
ORDER_MONGODB_DB = os.getenv('ORDER_MONGODB_DB')

CART_SERVICE = os.getenv('CART_SERVICE_NAME')
CART_MONGODB_USER = os.getenv('CART_MONGODB_USER')
CART_MONGODB_PASSWORD = os.getenv('CART_MONGODB_PASSWORD')
CART_MONGODB_HOST = os.getenv('CART_MONGODB_HOST')
CART_MONGODB_DB = os.getenv('CART_MONGODB_DB')

def assemble_userdb_url() -> Any:
    return f"postgresql://{USER_POSTGRES_USER}:{USER_POSTGRES_PASSWORD}@{USER_POSTGRES_HOST}:{USER_POSTGRES_PORT}/{USER_POSTGRES_DB}"

def assemble_productdb_url() -> Any:
    return f"postgresql://{PRODUCT_POSTGRES_USER}:{PRODUCT_POSTGRES_PASSWORD}@{PRODUCT_POSTGRES_HOST}:{PRODUCT_POSTGRES_PORT}/{PRODUCT_POSTGRES_DB}"

def assemble_orderdb_url() -> Any:
    return f"mongodb://{ORDER_MONGODB_USER}:{ORDER_MONGODB_PASSWORD}@{ORDER_MONGODB_HOST}"

def assemble_cartdb_url() -> Any:
    return f"mongodb://{CART_MONGODB_USER}:{CART_MONGODB_PASSWORD}@{CART_MONGODB_HOST}"

USERDB_URL = assemble_userdb_url()
PRODUCTDB_URL = assemble_productdb_url()
ORDERDB_URL = assemble_orderdb_url()
CARTDB_URL = assemble_cartdb_url()