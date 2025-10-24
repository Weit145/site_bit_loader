from typing import Annotated

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.profiles.crud import clear_upload_dir, create_profile
from app.tasks.tasks import send_message
from app.users import crud, token
from app.users.dependens import (
    chek_regist,
    get_current_user,
    user_by_id_path,
    user_form_to_user_login,
)
from app.users.schemas import (
    Token,
    UserCreate,
    UserGet,
    UserLogin,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_200_OK)
async def create_user_end_point(
    user_create: Annotated[UserCreate,Depends(chek_regist)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> dict:
    user = await crud.create_user(session=session, user_create=user_create)
    await create_profile(
        user=user,
        session=session,
    )
    access_token = token.create_access_token(data={"sub": user.username})
    send_message.delay(token=access_token,username=user.username,email=user.email)
    return {"message": "Email send"}

@router.get("/confirm/", response_model=Token)
async def registration_confirmation_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    token_pod: str = Query(..., description="Токен подтверждения регистрации"),
)->Token:
    user = await crud.registration_confirmation(session=session,token_pod=token_pod)
    access_token = token.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")

@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me_user_end_point(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await crud.delete_user(session=session, user_id=current_user.id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_users_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await crud.delete_all_users(session=session)
    clear_upload_dir()


@router.post("/token/", response_model=Token)
async def login_for_access_token_end_point(
    form_data: Annotated[UserLogin, Depends(user_form_to_user_login)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> Token:
    user = await crud.authenticate_user(session=session, user=form_data)
    access_token = token.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me/", response_model=UserResponse)
async def read_me_user_end_point(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> UserResponse:
    return current_user


@router.get("/{user_id}/", response_model=UserGet)
async def get_user_by_id_end_point(
    user: Annotated[UserResponse, Depends(user_by_id_path)],
) -> UserResponse:
    return user
