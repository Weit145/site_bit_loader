from datetime import datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.profiles.utils.checks import check_name_file
from app.users.schemas import UserResponse


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


def delete_uploaded_file(filename: str) -> bool | None:
    upload_dir = Path("app/uploads")
    file_path = upload_dir / filename
    if file_path.exists() and file_path.is_file() and filename != "default.png":
        file_path.unlink()

def upload_dir() -> Path:
    upload_dir = Path("app/uploads")
    upload_dir.mkdir(exist_ok=True)
    return upload_dir

def file_extension(
    file: UploadFile,
    current_user: UserResponse,
) -> str:
    check_name_file(file)
    Extension = Path(file.filename).suffix.lower()
    return f"{current_user.id}_{int(datetime.now().timestamp())}{Extension}"
