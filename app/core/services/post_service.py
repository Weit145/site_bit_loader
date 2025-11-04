
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Post
from app.core.repositories.post_repository import IPostRepository
from app.core.schemas.post import UpdatePost


class SQLAlchemyPostRepository(IPostRepository):
    def __init__(self,  session:AsyncSession):
        self.session=session

    async def add_post(self, post)->None:
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)

    async def delete_all_posts(self)->None:
        stm = select(Post).order_by(Post.id)
        result = await self.session.execute(stm)
        posts = result.scalars().all()
        for post in posts:
            await self.session.delete(post)
        await self.session.commit()

    async def delete_post(self, post: Post)->None:
        await self.session.delete(post)
        await self.session.commit()

    async def get_all_posts(self) -> list[Post|None]:
        stm = select(Post).order_by(Post.id)
        result = await self.session.execute(stm)
        posts_db = list(result.scalars().all())
        return posts_db

    async def update_post(self, post: UpdatePost, post_to_redact: Post)-> Post:
        stmt = (
            update(Post)
            .where(Post.id == post_to_redact.id)
            .values(**post.model_dump(exclude={"post_id"}))
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return stmt

    async def get_post_by_id(self, post_id: int) -> Post | None:
        return await self.session.get(Post, post_id)
