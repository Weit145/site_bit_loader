from app.core.models import Post
from app.posts.utils.checks import check_post
from app.posts.utils.schemas import (
    CreatePost,
    OutPost,
)


def converter_create_post_to_post_db(post: CreatePost, user_id: int) -> Post:
    return Post(
        title=post.title,
        body=post.body,
        user_id=user_id
    )

def converter_postdb_to_post_out_list(
    posts_db: list[Post],
) -> list[OutPost]:
    new_posts: list[OutPost] = []
    for post in posts_db:
        out_post = converter_postdb_to_post_out(post)
        new_posts.append(out_post)
    return new_posts


def converter_postdb_to_post_out(post_db: Post | None) -> OutPost:
    check_post(post_db)
    return OutPost(
        title=post_db.title,
        body=post_db.body,
        user_name=post_db.user.username,
        id=post_db.id,
        name_img=post_db.user.profile.name_img,
    )
