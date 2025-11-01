from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Post
from app.posts.schemas import (
    CreatePost,
    OutPost,
    UpdatePost,
)
from app.users.schemas import UserResponse


class IPostService(ABC):

    # Post
    @abstractmethod
    async def create_post(self, session: AsyncSession, post: CreatePost, current_user: UserResponse) -> OutPost:
        pass

    @abstractmethod
    async def delete_postdb_by_id(self, current_user: UserResponse, post_db: Post, session: AsyncSession) -> None:
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
