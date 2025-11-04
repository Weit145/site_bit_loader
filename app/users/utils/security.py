from app.core.config import settings
from jwt.exceptions import InvalidTokenError
from fastapi import Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.users.utils.checks import check_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth/token")

def get_password_hash(password) -> str:
    return settings.pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return settings.pwd_context.verify(plain_password, hashed_password)

async def decode_jwt_username(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        check_access_token(username)
        return username
    except InvalidTokenError:
        check_access_token(None)

async def decode_jwt_email(
    token: str,
)->str|None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email = payload.get("sub")
        check_access_token(email)
        return email
    except InvalidTokenError:
        check_access_token(None)