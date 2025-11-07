from typing import Annotated

from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.posts.services.post_service import PostService

router = APIRouter(prefix="/admin")

@router.delete("/all/", status_code=status.HTTP_204_NO_CONTENT)
async def dellete_all_posts_end_point(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    print("DEBUG HEADERS:", request.headers)
    await PostService().delete_all_posts(session=session)
