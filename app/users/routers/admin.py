from typing import Annotated

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.profiles.crud import clear_upload_dir
from app.users import crud
from app.users.schemas import (
    UserGet,
    UserResponse,
)

from app.users.services.user_service import UserService 

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

@router.get("/{user_id}/", response_model=UserGet)
async def get_user_by_id_end_point(
    id: Annotated[int, Path(ge=1)],
) -> UserResponse:
    return await UserService().get_user_by_id(id)

