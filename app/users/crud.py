from core.config import settings
from core.models import User
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreate, UserLogin, UserResponse

# Создание User


async def Create_User(session: AsyncSession, user_create: UserCreate) -> UserResponse:
    user_db = await Get_User(session=session, username=user_create.username)
    Check_User_Regist(user_db)
    use_and_password = Add_Password_Userdb(user_create)
    session.add(use_and_password)
    await session.commit()
    await session.refresh(use_and_password)
    return UserResponse.model_validate(use_and_password)


def Check_User_Regist(
    user_db: User | None,
) -> None:
    if user_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )


def Add_Password_Userdb(user_create: UserCreate) -> User:
    hashed_password = Get_Password_Hash(user_create.password)
    user_data = user_create.model_dump()
    user_data["password"] = hashed_password
    user_db = User(**user_data)
    return user_db


def Get_Password_Hash(password) -> str:
    return settings.pwd_context.hash(password)


# Удаление UserMe


async def Delete_User(session: AsyncSession, user_id: int) -> None:
    user_db = await session.get(User, user_id)
    Check_User(user_db)
    await session.delete(user_db)
    await session.commit()


def Check_User(
    user_db: User | None,
) -> None:
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


# Удаление все (ВООБЩЕ ВСЕГО)


async def Delete_All_Users(session: AsyncSession) -> None:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    for user in users:
        await session.delete(user)
    await session.commit()


# Вход в акаунт


async def Authenticate_User(
    session: AsyncSession,
    user: UserLogin,
) -> UserResponse:
    user_db = await Get_User(session=session, username=user.username)
    Check_Userdb_And_Password(user_db=user_db, password=user.password)
    return UserResponse.model_validate(user_db)


def Check_Userdb_And_Password(
    user_db: User | None,
    password: str,
) -> None:
    if (not user_db) or (not Verify_Password(password, user_db.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def Verify_Password(plain_password, hashed_password) -> bool:
    return settings.pwd_context.verify(plain_password, hashed_password)


async def Get_User(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user_db = result.scalar_one_or_none()
    return user_db
