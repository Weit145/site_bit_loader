import shutil
from datetime import datetime
from pathlib import Path as Path_oc
from typing import Annotated

from core.models import Profile, db_helper
from fastapi import Depends, HTTPException, Path, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from users.dependens import Get_Current_User
from users.schemas import UserResponse

from .schemas import ProfileResponse


async def profile_by_id(
    profile_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ProfileResponse:
    profile_db = await session.get(Profile, profile_id)
    if profile_db is not None:
        return ProfileResponse.model_validate(profile_db)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile {profile_id} not found"
    )


async def Check_File(
    file: UploadFile,
) -> UploadFile:
    if not file.content_type or not file.content_type.startswith("image/") or file.filename is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Problem file")
    return file


async def Profiledb_By_UserId(
    current_user: Annotated[UserResponse, Depends(Get_Current_User)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Profile:
    stmt = select(Profile).where(Profile.user_id == current_user.id)
    result = await session.execute(stmt)
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile {current_user.id} not found",
        )
    return profile


async def Add_Img_In_Folder(
    file: UploadFile,
    current_user: Annotated[UserResponse, Depends(Get_Current_User)],
) -> Profile:
    upload = upload_dir()
    unique_filename = file_extension(file=file, current_user=current_user)
    file_path = upload / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return Profile(
        name_img=unique_filename,
        img=True,
        user_id=current_user.id,
    )


def upload_dir() -> Path_oc:
    upload_dir = Path_oc("app/uploads")
    upload_dir.mkdir(exist_ok=True)
    return upload_dir


def file_extension(
    file: UploadFile,
    current_user: UserResponse,
) -> str:
    if file.filename is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dont open file")
    file_extension = Path_oc(file.filename).suffix.lower()
    return f"{current_user.id}_{int(datetime.now().timestamp())}{file_extension}"
