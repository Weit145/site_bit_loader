from fastapi import Depends, HTTPException, status

from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from .schemas import CreatePost, UpdatePost, PostBase, СorrectPost,PostResponse
from core.models import Post

async def create_post(
    session:AsyncSession,
    post_create:CreatePost
)->CreatePost:
    post=Post(**post_create.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post_create

async def delete_all(session:AsyncSession)->None:
    stm = select(Post).order_by(Post.id)
    result :Result  =await session.execute(stm)
    posts = result.scalars().all()
    for post in posts:
        await session.delete(post)
    await session.commit()

async def delete_by_id(
    session:AsyncSession,
    post:PostResponse,
    user_id:int
)->None:
    post_db = await session.get(Post, post.id)
    if post.user_id!=user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Is not your post"
        )
    await session.delete(post_db)
    await session.commit()

async def delete_by_user_id(
    session:AsyncSession,
    user_id:int
)->None:
    stm = select(Post).where(Post.user_id==user_id)
    result :Result  =await session.execute(stm)
    posts = result.scalars().all()
    for post in posts:
        await session.delete(post)
    await session.commit()

async def get_all(session:AsyncSession)->List[PostResponse]:
    stm = select(Post).order_by(Post.id)
    result :Result  =await session.execute(stm)
    return list(result.scalars().all())

async def update_post(
    session:AsyncSession, 
    post:UpdatePost,
    posts:PostResponse,
    user_id:int
)->PostResponse:
    if (not posts) or (posts.user_id!=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    stmt = (
        update(Post)
        .where(Post.id == posts.id)
        .values(**post.model_dump(exclude={'post_id'}))
        )
    await session.execute(stmt)
    await session.commit()

    stmt_select = select(Post).where(Post.id == posts.id)
    result = await session.execute(stmt_select)
    updated_post = result.scalar_one()

    return PostResponse.model_validate(updated_post)