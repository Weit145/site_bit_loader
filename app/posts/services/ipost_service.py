from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Post, User
from app.posts.utils.schemas import (
    CreatePost,
    OutPost,
    UpdatePost,
)


class IPostService(ABC):

    # Post
    @abstractmethod
    async def create_post(self, session: AsyncSession, post: CreatePost, current_user: User) -> OutPost:
        pass

    @abstractmethod
    async def delete_post(self, current_user: User, post_db: Post, session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def get_all_posts(self, session: AsyncSession) -> list[OutPost]:
        pass

    @abstractmethod
    async def get_by_id_post(self, post_db: Post) -> OutPost:
        pass

    @abstractmethod
    async def update_post(self, session: AsyncSession,post: UpdatePost, post_to_redact: Post) -> OutPost:
        pass


    # Admin
    @abstractmethod
    async def dellete_all_posts(self, session: AsyncSession) -> None:
        pass
