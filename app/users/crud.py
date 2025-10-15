from app.core.config import settings
from app.core.models import User
from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas import UserCreate, UserLogin, UserResponse

# Создание User


async def create_user(session: AsyncSession, user_create: UserCreate) -> UserResponse:
    user_db = await get_user(session=session, username=user_create.username)
    check_user_regist(user_db)
    user_with_hash = add_password_userdb(user_create)
    session.add(user_with_hash)
    await session.commit()
    await session.refresh(user_with_hash)
    return UserResponse.model_validate(user_with_hash)


def check_user_regist(
    user_db: User | None,
) -> None:
    if user_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )


def add_password_userdb(user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    user_data = user_create.model_dump()
    user_data["password"] = hashed_password
    user_db = User(**user_data)
    return user_db


def get_password_hash(password) -> str:
    return settings.pwd_context.hash(password)


# Удаление UserMe


async def delete_user(session: AsyncSession, user_id: int) -> None:
    user_db = await session.get(User, user_id)
    check_user(user_db)
    await session.delete(user_db)
    await session.commit()


def check_user(
    user_db: User | None,
) -> None:
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


# Удаление все (ВООБЩЕ ВСЕГО)


async def delete_all_users(session: AsyncSession) -> None:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    for user in users:
        await session.delete(user)
    await session.commit()


# Вход в акаунт


async def authenticate_user(
    session: AsyncSession,
    user: UserLogin,
) -> UserResponse:
    user_db = await get_user(session=session, username=user.username)
    check_userdb_and_password(user_db=user_db, password=user.password)
    return UserResponse.model_validate(user_db)


def check_userdb_and_password(
    user_db: User | None,
    password: str,
) -> None:
    if (not user_db) or (not verify_password(password, user_db.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_password(plain_password, hashed_password) -> bool:
    return settings.pwd_context.verify(plain_password, hashed_password)


async def get_user(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user_db = result.scalar_one_or_none()
    return user_db
