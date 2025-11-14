from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.models.user import User
from app.core.schemas.security import Cookies
from app.core.security.checks import (
    check_access_token,
    check_valid_refresh_token,
    check_user,
)
from app.core.security.password import (
    get_password_hash,
    verify_password,
)
from app.core.services.user_service import SQLAlchemyUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth/token/")

async def build_auth_response(session: AsyncSession, user_db: User) -> JSONResponse:
    access_token = create_access_token(data={"sub": user_db.username})
    cookie = await create_refresh_token(session=session, data={"sub": user_db.username}, user_db=user_db)
    response = JSONResponse(content={"access_token": access_token})
    response.set_cookie(
        key=cookie.key,
        value=cookie.value,
        httponly=cookie.httponly,
        secure=cookie.secure,
        samesite=cookie.samesite,
        max_age=cookie.max_age,
    )
    return response

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
    await SQLAlchemyUserRepository(session).add_refresh_token(user_db,hash_jwt)
    cookie = Cookies(key="refresh_token", value=encoded_jwt)
    return cookie


async def valid_refresh_token(session: AsyncSession,refresh_token:str):
    username = await decode_jwt_username(refresh_token)
    usr_db = await SQLAlchemyUserRepository(session).get_user_by_username(username)
    check_user(usr_db)
    result = verify_password(refresh_token,usr_db.refresh_token)
    check_valid_refresh_token(result)
    return username


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
