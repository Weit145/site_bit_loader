from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.models.db_hellper import db_helper
from app.users.services.user_service import UserService
from app.users.utils.dependens import (
    dependens_chek_regist,
)

router = APIRouter(prefix="/registration")

@router.post("/", status_code=status.HTTP_200_OK)
async def create_user_end_point(
    user: Annotated[User,Depends(dependens_chek_regist)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> dict:
    await UserService().create_user(session,user)
    return {"message": "Email send"}


@router.get("/confirm/",status_code=status.HTTP_200_OK)
async def registration_confirmation_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    token_pod: str = Query(..., description="Токен подтверждения регистрации"),
)->JSONResponse:
    response = await UserService().registration_confirmation(session,token_pod)
    return response
