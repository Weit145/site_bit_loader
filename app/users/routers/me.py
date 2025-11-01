from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.users.dependens import (
    get_current_user,
)
from app.users.schemas import (
    UserResponse,
)

from app.users.services.user_service import UserService 

router = APIRouter(prefix="/me")

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me_user_end_point(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await UserService().delete_me_user(current_user,session)

@router.get("/", response_model=UserResponse)
async def read_me_user_end_point(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> UserResponse:
    return await UserService().read_me_user(current_user)
