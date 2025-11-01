from app.core.config import settings
from app.core.models import User
from app.users.schemas import UserCreate


def add_password_userdb(user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    user_data = user_create.model_dump()
    user_data["password"] = hashed_password
    user_db = User(**user_data)
    return user_db

def get_password_hash(password) -> str:
    return settings.pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return settings.pwd_context.verify(plain_password, hashed_password)

