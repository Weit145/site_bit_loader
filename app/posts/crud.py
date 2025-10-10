from fastapi import  HTTPException, status

from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from .schemas import UpdatePost, OutPost,CreatePost
from core.models import Post

async def Create_Post(
    session:AsyncSession,
    post_create:CreatePost,
    user_id: int
)->OutPost:
    post = Post(
        title=post_create.title,
        body=post_create.body,
        user_id=user_id 
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return OutPost(
        id=post.id,
        title=post.title,
        body=post.body,
        user_name=post.user.username,
    )


async def Dellete_All_Posts(session:AsyncSession)->None:
    stm = select(Post).order_by(Post.id)
    result :Result  =await session.execute(stm)
    posts = result.scalars().all()
    for post in posts:
        await session.delete(post)
    await session.commit()

async def Delete_Postdb_By_Id(
    session:AsyncSession,
    post_db:Post,
    username:str
)->None:
    if post_db.user.username!=username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Is not your post"
        )
    await session.delete(post_db)
    await session.commit()


async def Get_All_Posts(session:AsyncSession)->List[OutPost]:
    stm = select(Post).order_by(Post.id)
    result :Result  =await session.execute(stm)
    posts_db=list(result.scalars().all())
    return Postdb_to_PostOut_list(posts_db=posts_db)

def Postdb_to_PostOut_list(
    posts_db:list[Post],
)->list[OutPost]:
    new_posts:list[OutPost]=[]  
    for post in posts_db:
        out_post=Postdb_To_PostOut(post)
        new_posts.append(out_post)
    return new_posts


async def Update_Post(
    session:AsyncSession, 
    post:UpdatePost,
    post_to_redact:Post,
    user_id:int
)->OutPost:
    Check_Post_And_User_Correct(
        post_to_redact=post_to_redact,
        user_id=user_id,
    )
    
    await Redact_Postdb(
        session=session,
        post_to_redact=post_to_redact,
        post=post,
    )
    post_db= await Update_Postdb(
        session=session,
        post_to_redact=post_to_redact,
    )
    return Postdb_To_PostOut(post_db=post_db)

def Check_Post_And_User_Correct(
    post_to_redact:Post,
    user_id:int
)->None:
    if (not post_to_redact) or (post_to_redact.user_id!=user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

async def Redact_Postdb(
    session:AsyncSession, 
    post_to_redact:Post,
    post:UpdatePost,
)->None:
    stmt = (
        update(Post)
        .where(Post.id == post_to_redact.id)
        .values(**post.model_dump(exclude={'post_id'}))
        )
    await session.execute(stmt)
    await session.commit()
    
async def Update_Postdb(
    session:AsyncSession, 
    post_to_redact:Post,
)->Post:
    stmt_select = select(Post).where(Post.id == post_to_redact.id)
    result = await session.execute(stmt_select)
    return result.scalar_one()


def Postdb_To_PostOut(
    post_db:Post|None
)->OutPost:
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return OutPost(
            title=post_db.title,
            body=post_db.body,
            user_name=post_db.user.username,
            id=post_db.id
        )
