from app.core.models import Post
from fastapi import HTTPException, status
from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.schemas import CreatePost, OutPost, UpdatePost

# Срздания поста


async def create_post(
    session: AsyncSession, post_create: CreatePost, user_id: int
) -> OutPost:
    post_db = Post(title=post_create.title, body=post_create.body, user_id=user_id)
    session.add(post_db)
    await session.commit()
    await session.refresh(post_db)
    return postdb_to_post_out(post_db=post_db)


# Удаление всех постов


async def dellete_all_posts(session: AsyncSession) -> None:
    stm = select(Post).order_by(Post.id)
    result: Result = await session.execute(stm)
    posts = result.scalars().all()
    for post in posts:
        await session.delete(post)
    await session.commit()


# Удаление по Id поста


async def delete_postdb_by_id(
    session: AsyncSession, post_db: Post, username: str
) -> None:
    if post_db.user.username != username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Is not your post"
        )
    await session.delete(post_db)
    await session.commit()


# Выввод всех постов


async def get_all_posts(session: AsyncSession) -> list[OutPost]:
    stm = select(Post).order_by(Post.id)
    result: Result = await session.execute(stm)
    posts_db = list(result.scalars().all())
    return postdb_to_post_out_list(posts_db=posts_db)


def postdb_to_post_out_list(
    posts_db: list[Post],
) -> list[OutPost]:
    new_posts: list[OutPost] = []
    for post in posts_db:
        out_post = postdb_to_post_out(post)
        new_posts.append(out_post)
    return new_posts


def postdb_to_post_out(post_db: Post | None) -> OutPost:
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return OutPost(
        title=post_db.title,
        body=post_db.body,
        user_name=post_db.user.username,
        id=post_db.id,
        name_img=post_db.user.profile.name_img,
    )


# Обновление поста по Id поста


async def update_post(
    session: AsyncSession,
    post: UpdatePost,
    post_to_redact: Post,
) -> OutPost:
    await redact_postdb(
        session=session,
        post_to_redact=post_to_redact,
        post=post,
    )
    post_db = await update_postdb(
        session=session,
        post_to_redact=post_to_redact,
    )
    return postdb_to_post_out(post_db=post_db)


async def redact_postdb(
    session: AsyncSession,
    post_to_redact: Post,
    post: UpdatePost,
) -> None:
    stmt = (
        update(Post)
        .where(Post.id == post_to_redact.id)
        .values(**post.model_dump(exclude={"post_id"}))
    )
    await session.execute(stmt)
    await session.commit()


async def update_postdb(
    session: AsyncSession,
    post_to_redact: Post,
) -> Post:
    stmt_select = select(Post).where(Post.id == post_to_redact.id)
    result = await session.execute(stmt_select)
    return result.scalar_one()
