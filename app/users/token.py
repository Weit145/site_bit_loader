from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt

async def decode_jwt(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        username = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        ).get("sub")
        check_user_log(username)
        return username
    except InvalidTokenError:
        check_user_log(None)

async def decode_jwt_reg(
    token: str,
)->str|None:
    try:
        email = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        ).get("sub")
        check_user_log(email)
        return email
    except InvalidTokenError:
        check_user_log(None)


def check_user_log(
    user_db: Any,
) -> None:
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
