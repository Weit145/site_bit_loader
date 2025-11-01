from abc import ABC, abstractmethod

from app.core.models import Post
from app.posts.schemas import UpdatePost


class IPostRepository(ABC):
    @abstractmethod
    async def add_post(self, post: Post)->None:
        pass

    @abstractmethod
    async def dellete_all_posts(self)->None:
        pass

    @abstractmethod
    async def dellete_post(self, post: Post) -> None:
        pass

    @abstractmethod
    async def get_all_posts(self) -> list[Post|None]:
        pass

    @abstractmethod
    async def update_post(self,post: UpdatePost, post_to_redact: Post) -> Post:
        pass

    @abstractmethod
    async def get_post_by_id(self, post_id: int) -> Post | None:
        pass
