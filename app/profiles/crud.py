from fastapi import Depends, HTTPException, status,UploadFile

from sqlalchemy import Result, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from pathlib import Path
import shutil
from datetime import datetime

from typing import List

from app.users.schemas import UserResponse
from .schemas import CreateProfile,ProfileResponse,ProfileBase
from core.models import Profile


def upload_dir()->Path:
    upload_dir = Path("app/uploads")
    upload_dir.mkdir(exist_ok=True)
    return upload_dir

def clear_upload_dir()->None:
    upload_dir = Path("app/uploads")
    if upload_dir.exists():
        shutil.rmtree(upload_dir)
    upload_dir.mkdir(exist_ok=True)

def delete_uploaded_file(filename: str) -> bool:
    upload_dir = Path("app/uploads")
    file_path = upload_dir / filename
    if file_path.exists() and file_path.is_file():
        file_path.unlink()

def file_extension(
    file:UploadFile,
    current_user:UserResponse,
)-> str:
    file_extension = Path(file.filename).suffix.lower()
    return f"{current_user.id}_{int(datetime.now().timestamp())}{file_extension}"

async def create_profile(
    file:UploadFile,
    current_user:UserResponse,
    session:AsyncSession,
)->ProfileResponse:
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    profile=await session.get(Profile, current_user.id)
    if profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user"
        )
    upload=upload_dir()
    if file.filename==None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    unique_filename = file_extension(file=file,current_user=current_user)
    file_path = upload / unique_filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    profile_create = CreateProfile(
        name_img=unique_filename,
        img=True,
        user_id=current_user.id
    )
    profile=Profile(**profile_create.model_dump())
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return ProfileResponse.model_validate(profile)


async def delete_all(
    session:AsyncSession,
)->None:
    stm = delete(Profile)
    result :Result  =await session.execute(stm)
    await session.commit()
    clear_upload_dir()
    
async def delete_profile(
    session: AsyncSession,
    user_id: int
)->None:
    stmt = select(Profile).where(Profile.user_id == user_id)
    result = await session.execute(stmt)
    existing_profile = result.scalar_one_or_none() 
    if not  existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    filename = existing_profile.name_img
    await session.delete(existing_profile)
    await session.commit()
    delete_uploaded_file(filename)
