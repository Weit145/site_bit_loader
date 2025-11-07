from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.models.db_hellper import db_helper
from app.core.security.dependens import (
    get_current_user,
)
from app.users.services.user_service import UserService
from app.users.utils.schemas import OutUser

router = APIRouter(prefix="/me")

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me_user_end_point(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await UserService().delete_me_user(current_user,session)

@router.get("/", response_model=OutUser)
async def read_me_user_end_point(
    current_user: Annotated[User, Depends(get_current_user)],
) -> OutUser:
    return await UserService().read_me_user(current_user)
