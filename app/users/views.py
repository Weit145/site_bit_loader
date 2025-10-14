from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_hellper import db_helper
from profiles.crud import Clear_Upload_dir, Create_Profile

from .dependens import (
    UserForm_TO_UserCreate,
    Get_Current_User,
    UserForm_TO_UserLogin,
    User_By_Id_Path,
)
from . import crud, token
from .schemas import (
    Token,
    UserCreate,
    UserGet,
    UserLogin,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=Token)
async def Create_User_EndPoint(
    user_create: Annotated[UserCreate, Depends(UserForm_TO_UserCreate)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> Token:
    user = await crud.Create_User(session=session, user_create=user_create)
    await Create_Profile(
        user=user,
        session=session,
    )
    access_token = token.Create_Access_Token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def Delete_Me_User_EndPoint(
    current_user: Annotated[UserResponse, Depends(Get_Current_User)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await crud.Delete_User(session=session, user_id=current_user.id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def Delete_All_Users_EndPoint(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await crud.Delete_All_Users(session=session)
    Clear_Upload_dir()


@router.post("/token/", response_model=Token)
async def Login_For_Access_Token_EndPoint(
    form_data: Annotated[UserLogin, Depends(UserForm_TO_UserLogin)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> Token:
    user = await crud.Authenticate_User(session=session, user=form_data)
    access_token = token.Create_Access_Token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me/", response_model=UserResponse)
async def Read_Me_User_EndPoint(
    current_user: Annotated[UserResponse, Depends(Get_Current_User)],
) -> UserResponse:
    return current_user


@router.get("/{user_id}/", response_model=UserGet)
async def Get_User_By_Id_EndPoint(
    user: Annotated[UserResponse, Depends(User_By_Id_Path)],
) -> UserResponse:
    return user
