from app.core.models import Post
from app.posts.schemas import OutPost
from app.posts.utils.checks import check_post


def postdb_to_post_out_list(
    posts_db: list[Post],
) -> list[OutPost]:
    new_posts: list[OutPost] = []
    for post in posts_db:
        out_post = postdb_to_post_out(post)
        new_posts.append(out_post)
    return new_posts


def postdb_to_post_out(post_db: Post | None) -> OutPost:
    check_post(post_db)
    return OutPost(
        title=post_db.title,
        body=post_db.body,
        user_name=post_db.user.username,
        id=post_db.id,
        name_img=post_db.user.profile.name_img,
    )
