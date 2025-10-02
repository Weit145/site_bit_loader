from fastapi import Depends, HTTPException, status

from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CreatePost, UpdatePost, BaseModel
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

async def delete_by_id(session:AsyncSession, post_id:int, user_id:int):
    post = await session.get(Post, post_id)
    await session.delete(post)
    await session.commit()

async def delete_by_user_id(session:AsyncSession, user_id:int):
    stm = select(Post).where(Post.user_id==user_id)
    result :Result  =await session.execute(stm)
    posts = result.scalars().all()
    for post in posts:
        await session.delete(post)
    await session.commit()

async def get_all(session:AsyncSession):
    stm = select(Post).order_by(Post.id)
    result :Result  =await session.execute(stm)
    return result.scalars().all()

async def update_post(session:AsyncSession, post:UpdatePost,posts:Post,user_id:int):
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
    await session.refresh(posts)
    return posts