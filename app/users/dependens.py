from typing import Annotated

from app.core.models import User, db_helper
from fastapi import Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.users import crud, token
from app.users.schemas import UserCreate, UserLogin, UserResponse


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


async def user_form_to_user_create(
    user_form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    try:
        user_create = UserCreate(
            username=user_form.username, password=user_form.password
        )
        return user_create
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Validation error"
        ) from None


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
    return UserResponse.model_validate(user_db)
