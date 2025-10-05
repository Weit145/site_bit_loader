from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .schemas import UserBase,UserResponse
from . import crud
from app.core.models import User
async def user_by_id(
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

async def user_by_username(
    username: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_dependency)
)->UserResponse:
    from . import crud 
    user_db = await crud.get_user(session, username)
    if user_db is not None:
        return UserResponse.model_validate(user_db)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {username} not found"
    )