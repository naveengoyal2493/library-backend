from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    ALLOWED_ORIGINS: list[str] = Field(default=["*"])
    DATABASE_URL: str
    BASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 20
    class Config:
        env_file = ".env"

settings = Settings()