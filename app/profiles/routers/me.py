from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.core.models.profile import Profile
from app.profiles import crud
from app.profiles.dependens import add_img_in_folder, profiledb_by_userid
from app.profiles.schemas import ProfileResponse

router = APIRouter(prefix="/me")

@router.put("/", response_model=ProfileResponse)
async def update_profile_end_point(
    new_profile: Annotated[Profile, Depends(add_img_in_folder)],
    profile: Annotated[Profile, Depends(profiledb_by_userid)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> ProfileResponse:
    return await crud.update_profile(
        new_profile=new_profile, profile=profile, session=session
    )

@router.put("/reset/", status_code=status.HTTP_205_RESET_CONTENT)
async def reset_me_end_point(
    profile: Annotated[Profile, Depends(profiledb_by_userid)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await crud.reset_profile(session=session, profile=profile)


@router.get("/", response_model=ProfileResponse)
async def read_me_profile_end_point(
    profile: Annotated[Profile, Depends(profiledb_by_userid)],
) -> ProfileResponse:
    return ProfileResponse.model_validate(profile)
