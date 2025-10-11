from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from core.models.db_hellper import db_helper  

from .schemas import UserCreate, Token, UserGet, UserResponse,UserLogin 
from . import crud
from . import dependens
from . import token

from profiles.crud import Create_Profile,Clear_Upload_dir

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=Token)
async def Create_User_EndPoint(
    user_create :  Annotated[UserCreate, Depends(dependens.UserForm_TO_UserCreate)],
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
    access_token = token.Create_Access_Token(data={"sub": user.username})
    return Token(
        access_token=access_token, 
        token_type="bearer"
    )
    


@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def Delete_Me_User_EndPoint(
    current_user: Annotated[UserResponse, Depends(dependens.Get_Current_User)],
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
    form_data: Annotated[UserLogin, Depends(dependens.UserForm_TO_UserLogin)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
) -> Token:
    user = await crud.Authenticate_User(
        session=session, 
        user=form_data
    )
    access_token = token.Create_Access_Token(data={"sub": user.username})
    return Token(
        access_token=access_token, 
        token_type="bearer"
    )

@router.get("/me/", response_model=UserResponse)  
async def Read_Me_User_EndPoint(
    current_user: Annotated[UserResponse, Depends(dependens.Get_Current_User)],
)->UserResponse:
    return current_user


@router.get("/{user_id}/", response_model=UserGet)
async def Get_User_By_Id_EndPoint(
    user:Annotated[ UserResponse, Depends(dependens.User_By_Id_Path)]
)->UserResponse:
    return user
