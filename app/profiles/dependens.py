from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ProfileResponse
from core.models import db_helper
from app.core.models import Profile
async def post_by_id(
    profile_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> ProfileResponse:
    profile_db = await session.get(Profile, profile_id)
    if profile_db is not None:
        return ProfileResponse.model_validate(profile_db)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post {profile_id} not found"
    )