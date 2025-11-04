from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.core.models.profile import Profile
from app.profiles.services.profile_service import ProfileService
from app.profiles.utils.dependens import add_img_in_folder, profiledb_by_userid
from app.profiles.utils.schemas import ProfileOut

router = APIRouter(prefix="/me")

@router.put("/", response_model=ProfileOut)
async def update_profile_end_point(
    new_profile: Annotated[Profile, Depends(add_img_in_folder)],
    profile: Annotated[Profile, Depends(profiledb_by_userid)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> ProfileOut:
    return await ProfileService().update_profile(session=session, profile=profile, new_profile=new_profile)

@router.put("/reset/", status_code=status.HTTP_205_RESET_CONTENT)
async def reset_me_end_point(
    profile: Annotated[Profile, Depends(profiledb_by_userid)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> ProfileOut:
    return await ProfileService().reset_me(session=session, profile=profile)


@router.get("/", response_model=ProfileOut)
async def read_me_profile_end_point(
    profile: Annotated[Profile, Depends(profiledb_by_userid)],
) -> ProfileOut:
    return await ProfileService().read_me_profile(profile=profile)
