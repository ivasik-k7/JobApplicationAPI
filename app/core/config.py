import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
    HASH_ALGORITHM: str = os.environ.get("HASH_ALGORITHM", "md5")
    HASH_KEY: str = os.environ.get("HASH_KEY", "key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 10)

    class Config:
        env_file = ".env"


settings = Settings()
