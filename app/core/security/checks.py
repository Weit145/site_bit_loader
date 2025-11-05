from fastapi import HTTPException, UploadFile, status

from app.core.models import User


def check_valid_refresh_token(
    result:bool,
)->None:
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_access_token(
        target:str|None,
)->None:
    if target is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

def check_for_current(
    user_db:User|None,
)->None:
    if user_db is None or not user_db.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username no active email, send email",
        )

def check_name_file(
    file: UploadFile,
) -> None:
    if file.filename is None or not file.filename.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file name"
        )

def check_user(
    user_db: User | None,
) -> None:
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )