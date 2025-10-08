from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import PostResponse, OutPost
from core.models import db_helper
from app.core.models import Post,User
from app.users.schemas import UserResponse


async def post_by_id(
    post_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> PostResponse:
    post_db = await session.get(Post, post_id)
    if post_db is not None:
        return PostResponse.model_validate(post_db)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post {post_id} not found"
    )


async def post_id_user(
    post:Annotated[PostResponse, Depends(post_by_id)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->OutPost:
    user_db = await session.get(User, post.user_id)
    if user_db is not None:
        user = UserResponse.model_validate(user_db)
        return OutPost(title=post.title,body=post.body,user_name=user.username,id=post.id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {post.user_id} not found"
    )
