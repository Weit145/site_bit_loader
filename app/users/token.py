from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import jwt
from core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def Create_Access_Token(data: dict) -> str:
    to_encode = data.copy()
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def Decode_Jwt(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        username = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm]).get(
            "sub"
        )
        Check_User_Log(username)
        return username
    except InvalidTokenError:
        Check_User_Log(None)


def Check_User_Log(
    user_db: Any,
) -> None:
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
