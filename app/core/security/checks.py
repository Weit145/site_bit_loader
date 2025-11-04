from fastapi import HTTPException, status
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