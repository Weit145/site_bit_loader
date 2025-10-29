from pathlib import Path
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Profile
from app.profiles.schemas import ProfileResponse
from app.users.schemas import UserResponse

# Создание профеля испотлбзуеться user/views.py


async def check_profile_in_db_by_userid(
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


async def create_profile(
    user: Annotated[UserResponse, Depends(check_profile_in_db_by_userid)],
    session: AsyncSession,
) -> None:
    profile = Profile(name_img="default.png", img=False, user_id=user.id)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)


# Обновление аватарки


async def update_profile(
    new_profile: Profile,
    profile: Profile,
    session: AsyncSession,
) -> ProfileResponse:
    delete_uploaded_file(profile.name_img)
    profile.name_img = new_profile.name_img
    profile.img = new_profile.img
    await session.commit()
    await session.refresh(profile)
    return ProfileResponse.model_validate(profile)


# Полностью сброс всех профелей


async def reset_all_profile(
    session: AsyncSession,
) -> None:
    stm = select(Profile).where(Profile.img == 1)
    result: Result = await session.execute(stm)
    profile_db = list(result.scalars().all())
    for profile in profile_db:
        await reset_profile(session=session, profile=profile)
    clear_upload_dir()


def clear_upload_dir() -> None:
    upload_dir = Path("app/uploads")
    try:
        for item in upload_dir.iterdir():
            if item.is_file() and item.name != "default.png":
                item.unlink()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error clearing upload directory",
        ) from None


# Сброс Одного профеля


async def reset_profile(session: AsyncSession, profile: Profile) -> ProfileResponse:
    check_no_reset_profiledb(profile=profile)
    delete_uploaded_file(profile.name_img)
    await redact_profiledb_to_default(
        session=session,
        profile=profile,
    )
    return ProfileResponse.model_validate(profile)


def check_no_reset_profiledb(profile: Profile) -> None:
    if not profile or profile.name_img == "default.png":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


async def redact_profiledb_to_default(
    session: AsyncSession,
    profile: Profile,
) -> None:
    profile.name_img = "default.png"
    profile.img = False
    await session.commit()
    await session.refresh(profile)


def delete_uploaded_file(filename: str) -> bool | None:
    upload_dir = Path("app/uploads")
    file_path = upload_dir / filename
    if file_path.exists() and file_path.is_file() and filename != "default.png":
        file_path.unlink()


# Удаления всех провилей

async def delete_all_profile(session: AsyncSession) -> None:
    stmt = select(Profile).order_by(Profile.id)
    result: Result = await session.execute(stmt)
    profiles = result.scalars().all()
    for profile in profiles:
        await session.delete(profile)
    await session.commit()
