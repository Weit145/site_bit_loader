from fastapi import APIRouter, Depends, status, HTTPException,Query, UploadFile, File

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import Annotated

from pathlib import Path
import shutil
from datetime import datetime

from core.models.db_hellper import db_helper 
from core.models.profile import Profile 


from . import crud
from .schemas import CreateProfile,ProfileResponse,ProfileBase
from app.users.schemas import UserResponse
from users.crud import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/",response_model=ProfileResponse)
async def create_profile(
    file:Annotated[UploadFile,File(description="Image file")],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->ProfileResponse:
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    if !(await session.get(Profile, current_user.id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    if file.filename==None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    file_extension = Path(file.filename).suffix.lower()
    unique_filename = f"{current_user.id}_{int(datetime.now().timestamp())}{file_extension}"
    file_path = upload_dir / unique_filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    profile_create = CreateProfile(
        name_img=unique_filename,
        img=True,
        user_id=current_user.id
    )

    return await crud.create_profile(session=session, profile_create=profile_create)