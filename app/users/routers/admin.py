from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.profiles.crud import clear_upload_dir
from app.users import crud
from app.users.dependens import (
    user_by_id_path,
)
from app.users.schemas import (
    UserGet,
    UserResponse,
)

router = APIRouter(prefix="/admin")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_users_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await crud.delete_all_users(session=session)
    clear_upload_dir()

@router.get("/{user_id}/", response_model=UserGet)
async def get_user_by_id_end_point(
    user: Annotated[UserResponse, Depends(user_by_id_path)],
) -> UserResponse:
    return user
