from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

from app.core.models import Post


# async def post_by_id(
#     post_id: Annotated[int, Path],
#     session: AsyncSession = Depends(db_helper.session_dependency)
# ) -> Post:
#     post = await session.get(Post, post_id)
#     if post is not None:
#         return post
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Post {post_id} not found"
#     )