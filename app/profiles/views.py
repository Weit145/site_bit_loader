from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from core.models.db_hellper import db_helper 
from core.models.profile import Profile

from . import crud
from .schemas import ProfileResponse
from .dependens import Add_Img_In_Folder,Profiledb_By_UserId

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.put("/me/", response_model=ProfileResponse)
async def Update_Profile_EndPoint(
    new_profile:Annotated[Profile, Depends(Add_Img_In_Folder)],
    profile: Annotated[Profile, Depends(Profiledb_By_UserId)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->ProfileResponse:
    return await crud.Update_Profile(new_profile=new_profile,profile=profile,session=session)


@router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def Reset_All_Profiles_EndPoint(
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    return await crud.Reset_All_Profile(session=session)

@router.delete("/me/",status_code=status.HTTP_204_NO_CONTENT)
async def Reset_Me_EndPoint(
    profile: Annotated[Profile, Depends(Profiledb_By_UserId)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    return await crud.Reset_Profile(session=session,profile=profile)

@router.get("/me/", response_model=ProfileResponse)
async def read_profile_me(
    profile: Annotated[Profile, Depends(Profiledb_By_UserId)],
)->ProfileResponse:
    return ProfileResponse.model_validate(profile)