from typing import Annotated

from app.core.models import Post, db_helper
from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.dependens import get_current_user
from app.users.schemas import UserResponse


async def postdb_by_id(
    post_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Post:
    post_db = await session.get(Post, post_id)
    if post_db is not None:
        return post_db
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found"
    )


def check_post_and_user_correct(
    post_to_redact: Annotated[Post, Depends(postdb_by_id)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> Post:
    if (not post_to_redact) or (post_to_redact.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return post_to_redact
