import os
from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv
from passlib.context import CryptContext
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

load_dotenv()


class Setting(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = False

    secret_key: str = os.getenv("SECRET_KEY", "default-secret-key")
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    algorithm: str = os.getenv("ALGORITHM", "HS256")

    pwd_context: ClassVar[CryptContext] = CryptContext(
        schemes=["argon2"], deprecated="auto"
    )


settings = Setting()
