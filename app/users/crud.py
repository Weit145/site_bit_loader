from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from passlib.context import CryptContext
    
from app.core.models.db_hellper import db_helper
from core.models import User
from .schemas import UserCreate, UserResponse

SECRET_KEY = "5a489ff4a2cb133115c02d4ad6d2e2eb0324d11e5527332e8afba53426a6f335"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

async def AuthenticateUser(
    session: AsyncSession,
    username: str,
    password: str
)->UserResponse:
    user_db = await GetUser(
        session=session, 
        username=username
    )
    CheckUserdbAndPassword(
        user_db=user_db,
        password=password
    )
    return UserResponse.model_validate(user_db)

async def CreateUser(
    session: AsyncSession, 
    user_create: UserCreate
)->UserResponse:
    user_db= await GetUser(
        session=session,
        username=user_create.username
    )
    CheckUserRegist(user_db)
    use_and_password=AddPasswordUserdb(user_create)
    session.add(use_and_password)
    await session.commit()
    await session.refresh(use_and_password)
    return UserResponse.model_validate(use_and_password)


def CheckUserRegist(
    user_db:User|None,
)->None:
    if user_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

def CheckUserdbAndPassword(
    user_db:User|None,
    password: str,
)->None:
    if (not user_db) or (not VerifyPassword(password, user_db.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

def VerifyPassword(plain_password, hashed_password)->bool:
    return pwd_context.verify(plain_password, hashed_password)

def AddPasswordUserdb(
    user_create: UserCreate
)->User:
    hashed_password = GetPasswordHash(user_create.password)
    user_data = user_create.model_dump()
    user_data["password"] = hashed_password
    user_db = User(**user_data)
    return user_db


def GetPasswordHash(password)->str:
    return pwd_context.hash(password)

def CreateAccessToken(
    data: dict
)->str:
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def DecodeJwt(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        CheckUserLog(username)
        return username
    except InvalidTokenError:
        CheckUserLog(None)


async def GetCurrentUser(
    username: Annotated[str, Depends(DecodeJwt)],
    session: AsyncSession = Depends(db_helper.session_dependency)
)->UserResponse:
    user_db= await GetUser(session=session,username=username)
    CheckUserLog(user_db)
    return UserResponse.model_validate(user_db)

def CheckUserLog(
    user_db:any,
)->None:
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def GetUser(
    session: AsyncSession,
    username: str
)->User|None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def DeleteUser(
    session: AsyncSession,
    user_id: int
)->None:
    user_db = await session.get(User, user_id)
    CheckUser(user_db)
    await session.delete(user_db)
    await session.commit()

def CheckUser(
    user_db:User|None,
)->None:
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

async def DeleteUsers_all(
    session: AsyncSession
)->None:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    for user in users:
        await session.delete(user)
    await session.commit()