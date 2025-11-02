from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User, db_helper
from app.core.services.user_service import SQLAlchemyUserRepository
from app.users.schemas import UserCreate, UserLogin, UserResponse
from app.users.utils import token
from app.users.utils.checks import (
    check_email_reg,
    check_for_current,
    check_username_reg,
)
from app.users.utils.convert import convert_profiledb

# Смотрит что человек создал акк но не подтвердил

async def dependens_chek_regist(
    user:UserCreate,
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->User:
    await check_email_reg(user=user,session=session)
    await check_username_reg(user=user,session=session)
    user_db = convert_profiledb(user)
    return user_db


# Переводить из формы в класс Pydantic

async def user_form_to_user_login(
    user_form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    try:
        user_create = UserLogin(
            username=user_form.username, password=user_form.password,
        )
        return user_create
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Validation error"
        ) from None

# Проверяет токен и то что акаунт актевирован

async def get_current_user(
    username: Annotated[str, Depends(token.decode_jwt_username)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> UserResponse:
    user_db = await SQLAlchemyUserRepository(session).get_user_by_username(username)
    check_for_current(user_db)
    return UserResponse.model_validate(user_db)

