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
from users.crud import Get_Current_User

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/",response_model=ProfileResponse)
async def create_profile(
    file:Annotated[UploadFile,File(description="Image file")],
    current_user: Annotated[UserResponse, Depends(Get_Current_User)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->ProfileResponse:
    return await crud.create_profile(file=file,current_user=current_user,session=session)

@router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_all(
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    return await crud.delete_all(session=session)

@router.delete("/me/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user: Annotated[UserResponse, Depends(Get_Current_User)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    return await crud.delete_profile(session=session,user_id=current_user.id)

@router.get("/me/", response_model=ProfileResponse)
async def read_profile_me(
    current_user: Annotated[UserResponse, Depends(Get_Current_User)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
):
    return