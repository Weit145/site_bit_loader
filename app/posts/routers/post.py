from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.core.models.post import Post
from app.posts import crud
from app.posts.dependens import check_post_and_user_correct, postdb_by_id
from app.posts.schemas import CreatePost, OutPost, UpdatePost
from app.users.dependens import get_current_user
from app.users.schemas import UserResponse

router = APIRouter()


@router.post("/", response_model=OutPost)
async def create_post_end_point(
    post: CreatePost,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> OutPost:
    return await crud.create_post(
        post_create=post, user_id=current_user.id, session=session
    )


@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_postdb_by_id_end_point(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    post_db: Annotated[Post, Depends(postdb_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await crud.delete_postdb_by_id(
        session=session, post_db=post_db, username=current_user.username
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_posts_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> list[OutPost]:
    return await crud.get_all_posts(session=session)


@router.get("/{post_id}/", response_model=OutPost)
async def get_by_id_post_end_point(
    post_db: Annotated[Post, Depends(postdb_by_id)],
) -> OutPost:
    return crud.postdb_to_post_out(post_db=post_db)


@router.put("/{post_id}/", response_model=OutPost)
async def update_post_end_point(
    post: UpdatePost,
    post_to_redact: Annotated[Post, Depends(check_post_and_user_correct)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> OutPost:
    return await crud.update_post(
        session=session, post=post, post_to_redact=post_to_redact
    )
