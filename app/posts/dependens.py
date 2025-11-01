from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Post, db_helper
from app.core.services.post_service import SQLAlchemyPostRepository
from app.posts.utils.checks import (
    check_post,
)
from app.users.dependens import get_current_user
from app.users.schemas import UserResponse


async def postdb_by_id(
    post_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Post:
    post_db = await SQLAlchemyPostRepository(session).get_post_by_id(post_id)
    check_post(post_db)
    return post_db


def check_post_and_user_correct(
    post_to_redact: Annotated[Post, Depends(postdb_by_id)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> Post:
    if (not post_to_redact) or (post_to_redact.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return post_to_redact
