from app.core.config import settings


def get_password_hash(password) -> str:
    return settings.pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return settings.pwd_context.verify(plain_password, hashed_password)
