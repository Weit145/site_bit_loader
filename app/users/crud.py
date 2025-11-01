from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.models import User
from app.tasks.tasks import send_message
from app.users.schemas import UserCreate, UserLogin, UserResponse
from app.users.token import create_access_token, decode_jwt_reg

# Создание User

async def create_user(session: AsyncSession, user_create: UserCreate) -> UserResponse:
    user_with_hash = add_password_userdb(user_create)
    session.add(user_with_hash)
    await session.commit()
    await session.refresh(user_with_hash)
    return UserResponse.model_validate(user_with_hash)



def add_password_userdb(user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    user_data = user_create.model_dump()
    user_data["password"] = hashed_password
    user_db = User(**user_data)
    return user_db


def get_password_hash(password) -> str:
    return settings.pwd_context.hash(password)

# Активация user

async def registration_confirmation(
    session: AsyncSession,
    token_pod: str,
) -> User:
    email = await decode_jwt_reg(token=token_pod)
    user_db = await get_user_by_email(session=session, email=email)
    check_no_active(user_db)
    stmt = (
        update(User)
        .where(User.id == user_db.id)
        .values(active=True)
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(stmt)
    await session.commit()
    return user_db

async def get_user_by_email(session: AsyncSession, email:Any) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user_db = result.scalar_one_or_none()
    return user_db


def check_no_active(
    user_db:User |None,
)->None:
    if user_db is None or user_db.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already active",
        )


def send_email(user:User|UserResponse)->None:
    access_token = create_access_token(data={"sub": user.email})
    send_message.delay(token=access_token,username=user.username,email=user.email)


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
    
# Удаление всех не подтверждённых пользователей

async def dellete_all_no_comfirm_users(session: AsyncSession)->None:
    stm = select(User).where(User.active==0)
    result: Result = await session.execute(stm)
    users_db = list (result.scalars().all())
    for user in users_db:
        await session.delete(user)
    await session.commit()

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
) -> User:
    user_db = await get_user_by_username(session=session, username=user.username)
    check_active(user_db)
    check_userdb_and_password(user_db=user_db, password=user.password)
    return user_db


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

def check_active(
    user_db:User |None,
)->None:
    if user_db is None or not user_db.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_password(plain_password, hashed_password) -> bool:
    return settings.pwd_context.verify(plain_password, hashed_password)


async def get_user_by_username(session: AsyncSession, username:Any) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user_db = result.scalar_one_or_none()
    return user_db
