from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Post, User, db_helper
from app.core.security.dependens import get_current_user
from app.core.services.post_service import SQLAlchemyPostRepository
from app.posts.utils.checks import (
    check_post,
    check_post_and_user_correct,
)


async def dependens_postdb_by_id(
    post_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Post:
    post_db = await SQLAlchemyPostRepository(session).get_post_by_id(post_id)
    check_post(post_db)
    return post_db


def dependens_check_post_and_user_correct(
    post_to_redact: Annotated[Post, Depends(dependens_postdb_by_id)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Post:
    check_post_and_user_correct(post_to_redact, current_user)
    return post_to_redact
