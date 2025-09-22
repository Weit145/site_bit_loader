from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated

from core.models.db_hellper import db_helper  # Исправлена опечатка
from .schemas import Create_User, User, Token,AvtorUser
from . import crud
from .dependens import user_by_id  # Раскомментирован импорт

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])  # Добавлен префикс
ACCESS_TOKEN_EXPIRE_MINUTES = 60

@router.post("/", response_model=User)
async def create_user(
    user_in: Create_User,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.create_user(session=session, user_create=user_in)

@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    await session.delete(user)
    await session.commit()

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_all(
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    await crud.delete_users_all(session=session)

@router.get("/{user_id}/", response_model=User)
async def get_user(user: User = Depends(user_by_id)):
    return user

@router.post("/token/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> Token:
    user = await crud.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# @router.get("/me/", response_model=User)  
# async def read_users_me(
#     current_user: User= Depends(crud.get_current_active_user),
# ):
#     return current_user