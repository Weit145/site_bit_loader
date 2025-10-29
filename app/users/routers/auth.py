from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.users import crud, token
from app.users.dependens import (
    user_form_to_user_login,
)
from app.users.schemas import (
    Token,
    UserLogin,
)

router = APIRouter(prefix="/auth")

@router.get("/refresh/", response_model=Token)
async def refresh_token_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    refresh_token: Annotated[str,Cookie(...)]
)->Token:
    username = await token.update_token(session=session,refresh_token=refresh_token)
    access_token = token.create_access_token(data={"sub": username})
    return Token(access_token=access_token,token_type="bearer")

@router.post("/token/", status_code=status.HTTP_200_OK)
async def login_for_access_token_end_point(
    form_data: Annotated[UserLogin, Depends(user_form_to_user_login)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> JSONResponse:
    user_db = await crud.authenticate_user(session=session, user=form_data)
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
