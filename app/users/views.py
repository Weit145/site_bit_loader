from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from core.models.db_hellper import db_helper  
from .schemas import UserCreate, Token, UserBase, UserResponse
from . import crud
from .dependens import UserByIdPath,UserFormTOUserCreate

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=Token)
async def create_user(
    user_create :  Annotated[UserCreate, Depends(UserFormTOUserCreate)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)-> Token:
    user = await crud.CreateUser(
        session=session, 
        user_create=user_create
    )
    access_token = crud.CreateAccessToken(data={"sub": user.username})
    return Token(
        access_token=access_token, 
        token_type="bearer"
    )
    


@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user: Annotated[UserResponse, Depends(crud.GetCurrentUser)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    await crud.DeleteUser(
        session=session,
        user_id=current_user.id
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def DeleteUsers_all(
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    await crud.DeleteUsers_all(session=session)


@router.post("/token/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
) -> Token:
    user = await crud.AuthenticateUser(
        session=session, 
        username=form_data.username, 
        password=form_data.password
    )
    access_token = crud.CreateAccessToken(data={"sub": user.username})
    return Token(
        access_token=access_token, 
        token_type="bearer"
    )

@router.get("/me/", response_model=UserResponse)  
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(crud.GetCurrentUser)],
)->UserResponse:
    return current_user


@router.get("/{user_id}/", response_model=UserBase)
async def get_user(
    user:Annotated[ UserResponse, Depends(UserByIdPath)]
)->UserResponse:
    return user
