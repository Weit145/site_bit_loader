from fastapi import HTTPException, UploadFile, status

from app.core.models import Profile


async def check_no_profile_in_db(
    profile: Profile,
) -> None:
    if profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user",
        )

def check_profile(profile: Profile) -> None:
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user",
        )

def check_no_reset_profiledb(profile: Profile) -> None:
    if not profile or profile.name_img == "default.png":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Already reset"
        )

async def check_file(
    file: UploadFile,
) -> UploadFile:
    if (
        not file.content_type
        or not file.content_type.startswith("image/")
        or file.filename is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Problem file"
        )
    return file

def check_name_file(
    file: UploadFile,
) -> None:
    if file.filename is None or not file.filename.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file name"
        )
