from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.models import Post


async def Postdb_By_Id(
    post_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> Post:
    post_db = await session.get(Post, post_id)
    if post_db is not None:
        return post_db
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post {post_id} not found"
    )
