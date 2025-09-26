from fastapi import Depends, HTTPException, status

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CreatePost
from core.models import Post

async def create_post(session:AsyncSession, post_create:CreatePost):
    post=Post(**post_create.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post_create

async def delete_all(session:AsyncSession):
    stm = select(Post).order_by(Post.id)
    result :Result  =await session.execute(stm)
    posts = result.scalars().all()
    for post in posts:
        await session.delete(post)
    await session.commit()

async def delete_by_id(session:AsyncSession, post_id:int):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    await session.delete(post)
    await session.commit()

async def get_all(session:AsyncSession):
    stm = select(Post).order_by(Post.id)
    result :Result  =await session.execute(stm)
    return result.scalars().all()

async def get_by_id(session:AsyncSession, post_id:int):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post