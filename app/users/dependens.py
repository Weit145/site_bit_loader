from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import User
async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> User:
    user = await session.get(User, user_id)
    if user is not None:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
    )

async def user_by_username(
    username: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    from . import crud 
    user = await crud.get_user(session, username)
    if user is not None:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {username} not found"
    )