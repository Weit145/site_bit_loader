from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials,HTTPBearer,OAuth2PasswordBearer

from typing import Annotated

from core.models.db_hellper import db_helper  
from .schemas import UserCreate, Token, UserBase, UserResponse
from . import crud
from .dependens import user_by_id_path 

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=Token)
async def create_user(
    user_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)-> Token:
    try:
        user_in = UserCreate(username=user_form.username,password=user_form.password)
        user = await crud.create_user(session=session, user_create=user_in)
        access_token = crud.create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail="Validation error"
        )


@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user: Annotated[UserResponse, Depends(crud.get_current_user)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    await crud.delete_user(session=session,user_id=current_user.id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_all(
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    await crud.delete_users_all(session=session)


@router.post("/token/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
) -> Token:
    user = await crud.authenticate_user(session=session, username=form_data.username, password=form_data.password)
    access_token = crud.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me/", response_model=UserResponse)  
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(crud.get_current_user)],
)->UserResponse:
    return current_user


@router.get("/{user_id}/", response_model=UserBase)
async def get_user(
    user:Annotated[ UserBase, Depends(user_by_id_path)]
)->UserBase:
    return user
