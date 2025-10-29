from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.models.user import User
from app.users.schemas import Cookies

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth/token")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt

async def create_refresh_token(session: AsyncSession,data:dict, user_db:User) -> Cookies:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=settings.access_token_refresh_day)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    hash_jwt = get_password_hash(encoded_jwt)
    user_db.refresh_token=hash_jwt
    await session.commit()
    await session.refresh(user_db)
    cookie = Cookies(key="refresh_token", value=encoded_jwt)
    return cookie

def get_password_hash(password) -> str:
    return settings.pwd_context.hash(password)

async def update_token(session: AsyncSession,refresh_token:str):
    username = await decode_jwt_reg(refresh_token)
    from app.users.dependens import get_user_by_username
    usr_db = await get_user_by_username(session=session,username=username)
    if not verify_password(refresh_token,usr_db.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username

def verify_password(plain_password, hashed_password) -> bool:
    return settings.pwd_context.verify(plain_password, hashed_password)


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
