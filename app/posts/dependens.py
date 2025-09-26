from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Path, status

import jwt
from jwt.exceptions import InvalidTokenError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import db_helper
from app.core.models import Post,User
from app.users.crud import SECRET_KEY,ALGORITHM,oauth2_scheme

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

async def true_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user= result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return True