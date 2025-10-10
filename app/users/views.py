from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from core.models.db_hellper import db_helper  
from .schemas import UserCreate, Token, UserBase, UserResponse
from . import crud
from .dependens import User_By_Id_Path,UserForm_TO_UserCreate
from app.profiles.crud import Create_Profile,Clear_Upload_dir

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=Token)
async def Create_User_EndPoint(
    user_create :  Annotated[UserCreate, Depends(UserForm_TO_UserCreate)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)-> Token:
    user = await crud.Create_User(
        session=session, 
        user_create=user_create
    )
    await Create_Profile(
        user=user,
        session=session,
    )
    access_token = crud.Create_Access_Token(data={"sub": user.username})
    return Token(
        access_token=access_token, 
        token_type="bearer"
    )
    


@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def Delete_Me_User_EndPoint(
    current_user: Annotated[UserResponse, Depends(crud.Get_Current_User)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    await crud.Delete_User(
        session=session,
        user_id=current_user.id
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def Delete_All_Users_EndPoint(
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    await crud.Delete_All_Users(session=session)
    Clear_Upload_dir()


@router.post("/token/", response_model=Token)
async def Login_For_Access_Token_EndPoint(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
) -> Token:
    user = await crud.Authenticate_User(
        session=session, 
        username=form_data.username, 
        password=form_data.password
    )
    access_token = crud.Create_Access_Token(data={"sub": user.username})
    return Token(
        access_token=access_token, 
        token_type="bearer"
    )

@router.get("/me/", response_model=UserResponse)  
async def Read_Me_User_EndPoint(
    current_user: Annotated[UserResponse, Depends(crud.Get_Current_User)],
)->UserResponse:
    return current_user


@router.get("/{user_id}/", response_model=UserBase)
async def Get_User_By_Id_EndPoint(
    user:Annotated[ UserResponse, Depends(User_By_Id_Path)]
)->UserResponse:
    return user
