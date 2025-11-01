import shutil
from typing import Annotated

from fastapi import Depends, Path, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Profile, db_helper
from app.core.services.profile_servicr import SQLAlchemyProfileRepository
from app.profiles.schemas import ProfileResponse
from app.profiles.utils.checks import (
    check_file,
    check_profile,
)
from app.profiles.utils.convert import (
    convert_profiledb,
)
from app.profiles.utils.dir import (
    file_extension,
    upload_dir,
)
from app.users.dependens import get_current_user
from app.users.schemas import UserResponse


async def profile_by_id(
    profile_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ProfileResponse:
    profile_db = await SQLAlchemyProfileRepository.get_profile_by_id(profile_id, session)
    check_profile(profile_db)
    return convert_profiledb(profile_db)



async def profiledb_by_userid(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Profile:
    profile_db = await SQLAlchemyProfileRepository.get_profile_by_user_id(current_user.id, session)
    check_profile(profile_db)
    return profile_db

async def add_img_in_folder(
    file: Annotated[UploadFile, Depends(check_file)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
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
