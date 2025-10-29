from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.profiles import crud

router = APIRouter(prefix="/admin")

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_profiles_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    return await crud.delete_all_profile(session=session)


@router.put("/", status_code=status.HTTP_205_RESET_CONTENT)
async def reset_all_profiles_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    return await crud.reset_all_profile(session=session)
