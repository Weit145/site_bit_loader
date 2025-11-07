from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.users.services.user_service import UserService
from app.users.utils.dependens import (
    dependens_user_form_to_user_login,
)
from app.users.utils.schemas import (
    Token,
    UserLogin,
)

router = APIRouter(prefix="/auth")

@router.get("/refresh/", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh_access_token_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    refresh_token: Annotated[str,Cookie(...)]
)->Token:
    token = await UserService().refresh_token(session,refresh_token)
    return token

@router.post("/token/", status_code=status.HTTP_200_OK)
async def authenticate_user_end_point(
    user: Annotated[UserLogin, Depends(dependens_user_form_to_user_login)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> JSONResponse:
    response = await UserService().authenticate_user(user,session)
    return response
