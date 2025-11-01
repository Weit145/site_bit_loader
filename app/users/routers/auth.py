from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.users.dependens import (
    user_form_to_user_login,
)
from app.users.schemas import (
    Token,
    UserLogin,
)
from app.users.services.user_service import UserService

router = APIRouter(prefix="/auth")

@router.get("/refresh/", response_model=Token)
async def refresh_token_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    refresh_token: Annotated[str,Cookie(...)]
)->Token:
    token = await UserService().refresh_token(session,refresh_token)
    return token

@router.post("/token/", status_code=status.HTTP_200_OK)
async def login_for_access_token_end_point(
    user: Annotated[UserLogin, Depends(user_form_to_user_login)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> JSONResponse:
    response = await UserService().login_for_access(user,session)
    return response
