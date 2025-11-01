from fastapi import HTTPException, status

from app.core.models.post import Post


def check_post_owner(post_db: Post, username: str)->None:
    if post_db.user.username != username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Is not your post"
        )

def check_post(post_db:Post)->None:
    if post_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
