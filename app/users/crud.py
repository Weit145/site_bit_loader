from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import delete, select


from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel



from ..main import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,oauth2_scheme
from core.models import User
from .schemas import UserBase,Create_User,Token,TokenData


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# TODO
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],session:AsyncSession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = session.get(User, username)
    if user is None:
        raise credentials_exception
    return user

# TODO
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends(),],session:AsyncSession) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



async def create_user(session:AsyncSession, user_create:Create_User):
    user=User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return  user


async def delete_user(session:AsyncSession, user:UserBase):
    await session.delete(user)
    await session.commit()

async def get_user(session:AsyncSession, user_id):
    return await session.get(User, user_id)

async def delete_users_all(session:AsyncSession):
    stat=select(User).order_by(User.id)
    result:Result=await session.execute(stat)
    users=result.scalars().all()
    for user in users:
        await session.delete(user)
    await session.commit()