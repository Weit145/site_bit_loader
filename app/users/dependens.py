from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User, db_helper
from app.users import crud, token
from app.users.schemas import UserCreate, UserLogin, UserResponse
from app.tasks.tasks import send_message


async def chek_regist(
    user:UserCreate,
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->UserCreate:
    stmt = select(User).where(User.email==user.email)
    result= await session.execute(stmt)
    user_db = result.scalar_one_or_none()
    if user_db is not None and user_db.active==False:
        access_token = token.create_access_token(data={"sub": user.username})
        send_message.delay(token=access_token,username=user.username,email=user.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username no active email, send email",
        )
    await check_email_reg(user=user,session=session)
    await check_username_reg(user=user,session=session)
    return user

async def check_email_reg(
    user:UserCreate,
    session:AsyncSession
)->None:
    stmt = select(User).where(User.email==user.email)
    result= await session.execute(stmt)
    user_db = result.scalar_one_or_none()
    if user_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

async def check_username_reg(
    user: UserCreate,
    session: AsyncSession
) -> None:
    user_db = await get_user(session=session,username=user.username)
    if user_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

async def get_user(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user_db = result.scalar_one_or_none()
    return user_db



async def user_by_id_path(
    user_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> UserResponse:
    user_db = await session.get(User, user_id)
    if user_db is not None:
        return UserResponse.model_validate(user_db)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
    )

async def user_form_to_user_login(
    user_form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    try:
        user_create = UserLogin(
            username=user_form.username, password=user_form.password
        )
        return user_create
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Validation error"
        ) from None

async def get_current_user(
    username: Annotated[str, Depends(token.decode_jwt)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> UserResponse:
    user_db = await crud.get_user(session=session, username=username)
    token.check_user_log(user_db)
    check_active(user_db)
    return UserResponse.model_validate(user_db)

def check_active(
    user_db:User |None,
)->None:
    check_found_user(user_db)
    if user_db.active==False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def check_found_user(
    user_db:User|None,
)->None:
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )