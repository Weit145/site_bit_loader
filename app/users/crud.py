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

def verify_password(plain_password, hashed_password)->bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password)->str:
    return pwd_context.hash(password)

async def get_user(
    session: AsyncSession,
    username: str
)->User|None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str
)->UserResponse:
    user_db = await get_user(session, username)
    if (not user_db) or (not verify_password(password, user_db.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserResponse.model_validate(user_db)

def create_access_token(
    data: dict
)->str:
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def decode_jwt(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise credentials_exception
        else:
            return username
    except InvalidTokenError:
        raise credentials_exception

async def get_current_user(
    username: Annotated[str, Depends(decode_jwt)],
    session: AsyncSession = Depends(db_helper.session_dependency)
)->UserResponse:
    user_db= await get_user(session=session,username=username)
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserResponse.model_validate(user_db)


async def create_user(
    session: AsyncSession, 
    user_create: UserCreate
)->UserResponse:
    user_db= await get_user(session=session,username=user_create.username)
    if user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = get_password_hash(user_create.password)
    user_data = user_create.model_dump()
    user_data["password"] = hashed_password
    
    user_db = User(**user_data)
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return UserResponse.model_validate(user_db)

async def delete_user(
    session: AsyncSession,
    user_id: int
)->None:
    from app.posts.crud import delete_by_user_id
    await delete_by_user_id(session=session,user_id=user_id)
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    await session.delete(user)
    await session.commit()

async def delete_users_all(session: AsyncSession)->None:
    from app.posts.crud import delete_all
    await delete_all(session)
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    for user in users:
        await session.delete(user)
    await session.commit()