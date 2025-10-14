from pathlib import Path
from typing import Annotated

from core.models import Profile
from fastapi import Depends, HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from users.schemas import UserResponse

from .schemas import ProfileResponse

# Создание профеля испотлбзуеться user/views.py


async def Check_Profile_In_Db_By_UserId(
    user: UserResponse,
    session: AsyncSession,
) -> UserResponse:
    profile = await session.get(Profile, user.id)
    if profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user",
        )
    return user


async def Create_Profile(
    user: Annotated[UserResponse, Depends(Check_Profile_In_Db_By_UserId)],
    session: AsyncSession,
) -> None:
    profile = Profile(name_img="default.png", img=False, user_id=user.id)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)


# Обновление аватарки


async def Update_Profile(
    new_profile: Profile,
    profile: Profile,
    session: AsyncSession,
) -> ProfileResponse:
    Delete_Uploaded_File(profile.name_img)
    profile.name_img = new_profile.name_img
    profile.img = new_profile.img
    await session.commit()
    await session.refresh(profile)
    return ProfileResponse.model_validate(profile)


# Полностью сброс всех профелей


async def Reset_All_Profile(
    session: AsyncSession,
) -> None:
    stm = select(Profile).where(Profile.img == 1)
    result: Result = await session.execute(stm)
    profile_db = list(result.scalars().all())
    for profile in profile_db:
        await Reset_Profile(session=session, profile=profile)
    Clear_Upload_dir()


def Clear_Upload_dir() -> None:
    Upload_Dir = Path("app/uploads")
    try:
        for item in Upload_Dir.iterdir():
            if item.is_file() and item.name != "default.png":
                item.unlink()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error clearing upload directory",
        ) from None


# Сброс Одного профеля


async def Reset_Profile(session: AsyncSession, profile: Profile) -> ProfileResponse:
    Check_No_Reset_Profiledb(profile=profile)
    Delete_Uploaded_File(profile.name_img)
    await Redact_Profiledb_to_Default(
        session=session,
        profile=profile,
    )
    return ProfileResponse.model_validate(profile)


def Check_No_Reset_Profiledb(profile: Profile) -> None:
    if not profile or profile.name_img == "default":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


async def Redact_Profiledb_to_Default(
    session: AsyncSession,
    profile: Profile,
) -> None:
    profile.name_img = "default.png"
    profile.img = False
    await session.commit()
    await session.refresh(profile)


def Delete_Uploaded_File(filename: str) -> bool | None:
    Upload_Dir = Path("app/uploads")
    file_path = Upload_Dir / filename
    if file_path.exists() and file_path.is_file() and filename != "default.png":
        file_path.unlink()
