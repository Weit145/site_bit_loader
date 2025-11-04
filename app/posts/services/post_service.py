from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.post import Post, User
from app.core.services.post_service import SQLAlchemyPostRepository
from app.posts.services.ipost_service import IPostService
from app.posts.utils.checks import (
    check_post_owner,
)
from app.posts.utils.converter import (
    converter_create_post_to_post_db,
    converter_postdb_to_post_out,
    converter_postdb_to_post_out_list,
)
from app.posts.utils.schemas import (
    CreatePost,
    OutPost,
    UpdatePost,
)


class PostService(IPostService):

    # Post
    async def create_post(self, session: AsyncSession, post: CreatePost, current_user: User) -> OutPost:
        post_db = converter_create_post_to_post_db(post, current_user.id)
        await SQLAlchemyPostRepository(session).add_post(post_db)
        return converter_postdb_to_post_out(post_db)

    async def delete_post(self, current_user: User, post_db: Post, session: AsyncSession) -> None:
        check_post_owner(post_db, current_user.username)
        await SQLAlchemyPostRepository(session).delete_post(post_db)

    async def get_all_posts(self, session: AsyncSession) -> list[OutPost]:
        posts_db = await SQLAlchemyPostRepository(session).get_all_posts()
        return converter_postdb_to_post_out_list(posts_db)

    async def get_by_id_post(self, post_db: Post) -> OutPost:
        return converter_postdb_to_post_out(post_db)

    async def update_post(self, session: AsyncSession, post: UpdatePost, post_to_redact: Post) -> OutPost:
        post_db = await SQLAlchemyPostRepository(session).update_post(post, post_to_redact)
        return converter_postdb_to_post_out(post_db)


    # Admin
    async def delete_all_posts(self, session: AsyncSession) -> None:
        await SQLAlchemyPostRepository(session).delete_all_posts()
