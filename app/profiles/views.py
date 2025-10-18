from typing import Annotated

from app.core.models.db_hellper import db_helper
from app.core.models.profile import Profile
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.profiles import crud
from app.profiles.dependens import add_img_in_folder, profiledb_by_userid
from app.profiles.schemas import ProfileResponse

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.put("/me/", response_model=ProfileResponse)
async def update_profile_end_point(
    new_profile: Annotated[Profile, Depends(add_img_in_folder)],
    profile: Annotated[Profile, Depends(profiledb_by_userid)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> ProfileResponse:
    return await crud.update_profile(
        new_profile=new_profile, profile=profile, session=session
    )

@router.delete("/delete_all/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_profiles_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    return await crud.delete_all_profile(session=session)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def reset_all_profiles_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    return await crud.reset_all_profile(session=session)


@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def reset_me_end_point(
    profile: Annotated[Profile, Depends(profiledb_by_userid)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await crud.reset_profile(session=session, profile=profile)


@router.get("/me/", response_model=ProfileResponse)
async def read_me_profile_end_point(
    profile: Annotated[Profile, Depends(profiledb_by_userid)],
) -> ProfileResponse:
    return ProfileResponse.model_validate(profile)
