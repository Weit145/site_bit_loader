from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.profiles.crud import create_profile
from app.users import crud, token
from app.users.dependens import (
    chek_regist,
)
from app.users.schemas import (
    UserCreate,
)

router = APIRouter(prefix="/registration")

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
    crud.send_email(user)
    return {"message": "Email send"}


@router.get("/confirm/",status_code=status.HTTP_200_OK)
async def registration_confirmation_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    token_pod: str = Query(..., description="Токен подтверждения регистрации"),
)->JSONResponse:
    user_db = await crud.registration_confirmation(session=session,token_pod=token_pod)
    access_token = token.create_access_token(data={"sub": user_db.username})
    cookie = await token.create_refresh_token(session=session,data={"sub": user_db.username},user_db=user_db)
    response = JSONResponse(content={"access_token":access_token})
    response.set_cookie(
        key=cookie.key,
        value=cookie.value,
        httponly=cookie.httponly,
        secure=cookie.secure,
        samesite=cookie.samesite,
        max_age=cookie.max_age
    )
    return response
