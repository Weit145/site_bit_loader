from fastapi import Depends, HTTPException, status,UploadFile

from sqlalchemy import Result, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from pathlib import Path
import shutil
from datetime import datetime

from typing import List

from app.users.schemas import UserResponse
from .schemas import CreateProfile,ProfileResponse
from core.models import Profile


async def Create_Profile(
    file:UploadFile,
    current_user:UserResponse,
    session:AsyncSession,
)->ProfileResponse:
    Check_File(file=file)
    await Check_Profile_In_Db_By_UserId(
        current_user=current_user,
        session=session
    )
    profile_create = await Add_Img_In_Folder(
        file=file,
        current_user=current_user,
    )
    profile=Profile(**profile_create.model_dump())
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return ProfileResponse.model_validate(profile)

def Check_File(
    file:UploadFile,
)->None:
    if not file.content_type or not file.content_type.startswith('image/') or file.filename==None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Problen file"
        )

async def Check_Profile_In_Db_By_UserId(
    current_user:UserResponse,
    session:AsyncSession,
)->None:
    profile=await session.get(Profile, current_user.id)
    if profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user"
        )

async def Add_Img_In_Folder(
    file:UploadFile,
    current_user:UserResponse,
)->CreateProfile:
    upload=upload_dir()
    unique_filename = file_extension(
        file=file,
        current_user=current_user
    )
    file_path = upload / unique_filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return CreateProfile(
        name_img=unique_filename,
        img=True,
        user_id=current_user.id
    )

def upload_dir()->Path:
    upload_dir = Path("app/uploads")
    upload_dir.mkdir(exist_ok=True)
    return upload_dir

def file_extension(
    file:UploadFile,
    current_user:UserResponse,
)-> str:
    if file.filename==None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dont open file"
        )
    file_extension = Path(file.filename).suffix.lower()
    return f"{current_user.id}_{int(datetime.now().timestamp())}{file_extension}"


def delete_uploaded_file(filename: str) -> bool|None:
    upload_dir = Path("app/uploads")
    file_path = upload_dir / filename
    if file_path.exists() and file_path.is_file():
        file_path.unlink()

async def Delete_All_Profile(
    session:AsyncSession,
)->None:
    stm = delete(Profile)
    result :Result  =await session.execute(stm)
    await session.commit()
    Clear_Upload_dir()

def Clear_Upload_dir()->None:
    upload_dir = Path("app/uploads")
    if upload_dir.exists():
        shutil.rmtree(upload_dir)
    upload_dir.mkdir(exist_ok=True)

    
async def Delete_Profile(
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


