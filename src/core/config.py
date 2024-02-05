import secrets
from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    SECRET_KEY: str = "aa7d737421b91a5cee8d014f68b0db13bb34034d833cbca5c064af23105250c7"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    EMAIL_TEST_USER: EmailStr = "test@example.com"
    FIRST_SUPERUSER: EmailStr = "admin@admin.com"
    FIRST_SUPERUSER_PASSWORD: str =  "admin"
    
    
settings = Settings()