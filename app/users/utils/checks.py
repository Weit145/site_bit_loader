from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.services.user_service import SQLAlchemyUserRepository
from app.users.schemas import UserCreate
from app.users.utils.password import verify_password


def check_for_regist(
    user_db:User|None,
)->None:
    if user_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username no active email, send email",
        )

def check_for_current(
    user_db:User|None,
)->None:
    if check_user(user_db) or check_active(user_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username no active email, send email",
        )
def check_for_auth(
    user_db:User|None,
    password: str,
)->None:
    if check_user(user_db) or check_userdb_and_password(user_db,password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username problem",
        )

def check_no_active(
    user_db:User|None,
)->None:
    if check_user(user_db) or user_db.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already active",
        )

def check_active(
    user_db:User,
)->None:
    if not user_db.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active",
            headers={"WWW-Authenticate": "Bearer"},
        )

def check_user(
    user_db: User | None,
) -> None:
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


def check_userdb_and_password(
    user_db: User,
    password: str,
) -> None:
    if not (verify_password(password, user_db.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def check_email_reg(
    user:UserCreate,
    session:AsyncSession
)->None:
    user_db = await SQLAlchemyUserRepository(session).get_user_by_email(user.email)
    if user_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )


async def check_username_reg(
    user: UserCreate,
    session: AsyncSession
) -> None:
    user_db = await SQLAlchemyUserRepository(session).get_user_by_username(user.username)
    if user_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

def check_valid_refresh_token(
    result:bool,
)->None:
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_access_token(
        target:str|None,
)->None:
    if target is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
