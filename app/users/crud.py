from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

    
from app.core.models.db_hellper import db_helper
from core.models import User
from .schemas import UserCreate, UserResponse
from app.core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

# Создание User

async def Create_User(
    session: AsyncSession, 
    user_create: UserCreate
)->UserResponse:
    user_db= await Get_User(
        session=session,
        username=user_create.username
    )
    Check_User_Regist(user_db)
    use_and_password=Add_Password_Userdb(user_create)
    session.add(use_and_password)
    await session.commit()
    await session.refresh(use_and_password)
    return UserResponse.model_validate(use_and_password)

def Check_User_Regist(
    user_db:User|None,
)->None:
    if user_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

def Add_Password_Userdb(
    user_create: UserCreate
)->User:
    hashed_password = Get_Password_Hash(user_create.password)
    user_data = user_create.model_dump()
    user_data["password"] = hashed_password
    user_db = User(**user_data)
    return user_db

def Get_Password_Hash(password)->str:
    return settings.pwd_context.hash(password)


# Удаление UserMe

async def Delete_User(
    session: AsyncSession,
    user_id: int
)->None:
    user_db = await session.get(User, user_id)
    Check_User(user_db)
    await session.delete(user_db)
    await session.commit()

def Check_User(
    user_db:User|None,
)->None:
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


# Удаление все (ВООБЩЕ ВСЕГО)

async def Delete_All_Users(
    session: AsyncSession
)->None:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    for user in users:
        await session.delete(user)
    await session.commit()
    Clear_Upload_dir()
    


# Вход в акаунт
    
async def Authenticate_User(
    session: AsyncSession,
    username: str,
    password: str
)->UserResponse:
    user_db = await Get_User(
        session=session, 
        username=username
    )
    Check_Userdb_And_Password(
        user_db=user_db,
        password=password
    )
    return UserResponse.model_validate(user_db)

def Check_Userdb_And_Password(
    user_db:User|None,
    password: str,
)->None:
    if (not user_db) or (not Verify_Password(password, user_db.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

def Verify_Password(plain_password, hashed_password)->bool:
    return settings.pwd_context.verify(plain_password, hashed_password)


# СОздание токена (Вход в акаунт)

def Create_Access_Token(
    data: dict
)->str:
    to_encode = data.copy()
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt



# Проверка User на вход в акаунт
async def Decode_Jwt(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        username = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm]).get("sub")
        Check_User_Log(username)
        return username
    except InvalidTokenError:
        Check_User_Log(None)


async def Get_Current_User(
    username: Annotated[str, Depends(Decode_Jwt)],
    session: AsyncSession = Depends(db_helper.session_dependency)
)->UserResponse:
    user_db= await Get_User(session=session,username=username)
    Check_User_Log(user_db)
    return UserResponse.model_validate(user_db)


def Check_User_Log(
    user_db:Any,
)->None:
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def Get_User(
    session: AsyncSession,
    username: str
)->User|None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
