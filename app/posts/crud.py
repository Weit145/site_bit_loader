from fastapi import  HTTPException, status

from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from .schemas import UpdatePost, OutPost,PostResponse,CreatePost
from core.models import Post
from app.users.dependens import UserById
from .dependens import post_id_user

async def create_post(
    session:AsyncSession,
    post_create:CreatePost,
    user_id: int
)->PostResponse:
    post = Post(
        title=post_create.title,
        body=post_create.body,
        user_id=user_id 
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return PostResponse.model_validate(post)


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

async def postResponse_to_postOut_list(
    posts:list[PostResponse],
    session:AsyncSession
)->list[OutPost]:
    new_posts:list[OutPost]=[]
    for post in posts:
        username=await UserById(
            user_id=post.user_id,
            session=session
        )
        out_post=OutPost(
            title=post.title,
            body=post.body,
            user_name=username.username,
            id=post.id
        )
        new_posts.append(out_post)
    return new_posts

async def get_all(session:AsyncSession)->List[OutPost]:
    stm = select(Post).order_by(Post.id)
    result :Result  =await session.execute(stm)
    posts=list(result.scalars().all())
    return await postResponse_to_postOut_list(posts=posts,session=session)

async def update_post(
    session:AsyncSession, 
    post:UpdatePost,
    post_to_redact:PostResponse,
    user_id:int
)->OutPost:
    if (not post_to_redact) or (post_to_redact.user_id!=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    stmt = (
        update(Post)
        .where(Post.id == post_to_redact.id)
        .values(**post.model_dump(exclude={'post_id'}))
        )
    await session.execute(stmt)
    await session.commit()

    stmt_select = select(Post).where(Post.id == post_to_redact.id)
    result = await session.execute(stmt_select)
    updated_post = result.scalar_one()
    post=PostResponse.model_validate(updated_post)
    return await post_id_user(post=post,session=session)