from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.core.services.user_service import SQLAlchemyUserRepository
from app.core.models.user import User
from app.core.security.token import decode_jwt_username
from app.core.security.checks import (
    check_for_current,
)

async def get_current_user(
    username: Annotated[str, Depends(decode_jwt_username)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    user_db = await SQLAlchemyUserRepository(session).get_user_by_username(username)
    check_for_current(user_db)
    return user_db
