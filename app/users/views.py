from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials,HTTPBearer,OAuth2PasswordBearer
from datetime import timedelta
from typing import Annotated

from core.models.db_hellper import db_helper  
from .schemas import Create_User, User, Token, AvtorUser
from . import crud
from .dependens import user_by_id  

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.post("/", response_model=Token)
async def create_user(
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)-> Token:
    user_in = Create_User(username=user.username,password=user.password)
    user = await crud.create_user(session=session, user_create=user_in)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    current_user: Annotated[User, Depends(crud.get_current_user)],
    user: Annotated[User, Depends(user_by_id)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
):
    if user.id!=current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not you ID"
        )
    await crud.delete_user(session=session,user_id=user.id)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_all(
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
):
    await crud.delete_users_all(session=session)


@router.post("/token/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
) -> Token:
    user = await crud.authenticate_user(session, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me/", response_model=User)  
async def read_users_me(
    current_user: Annotated[User, Depends(crud.get_current_user)],
):
    return current_user


@router.get("/{user_id}/", response_model=User)
async def get_user(
    user:Annotated[ User, Depends(user_by_id)]
)->User:
    return user
