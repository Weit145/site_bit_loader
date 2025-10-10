from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import db_helper
from .schemas import UserResponse,UserCreate
from app.core.models import User



async def User_By_Id_Path(
    user_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> UserResponse:
    user_db = await session.get(User, user_id)
    if user_db is not None:
        return UserResponse.model_validate(user_db)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
    )

async def UserForm_TO_UserCreate(
    user_form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    try:
        user_create = UserCreate(
            username=user_form.username,
            password=user_form.password
        )
        return user_create
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error"
        )