from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.posts.services.post_service import PostService

router = APIRouter(prefix="/admin")

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def dellete_all_posts_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await PostService().delete_all_posts(session=session)
