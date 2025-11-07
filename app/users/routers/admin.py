from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.users.services.user_service import UserService
from app.users.utils.schemas import (
    OutUser,
)

router = APIRouter(prefix="/admin")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_users_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await UserService().delete_all_users(session)

@router.delete("/nocomfirm/",status_code = status.HTTP_204_NO_CONTENT)
async def dellete_all_no_comfirm_users_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
)->None:
    await UserService().dellete_all_no_comfirm_users(session)

@router.get("/{user_id}/", response_model=OutUser)
async def get_user_by_id_end_point(
    user_id: Annotated[int, Path(ge=1)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> OutUser:
    return await UserService().get_user_by_id(user_id, session)

