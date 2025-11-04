from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_hellper import db_helper
from app.core.models.post import (
    Post,
    User,
)
from app.core.security.dependens import get_current_user
from app.posts.services.post_service import PostService
from app.posts.utils.dependens import (
    dependens_check_post_and_user_correct,
    dependens_postdb_by_id,
)
from app.posts.utils.schemas import (
    CreatePost,
    OutPost,
    UpdatePost,
)

router = APIRouter()


@router.post("/", response_model=OutPost)
async def create_post_end_point(
    post: CreatePost,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> OutPost:
    return await PostService().create_post(
        session=session, post=post, current_user=current_user
    )


@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_postdb_by_id_end_point(
    current_user: Annotated[User, Depends(get_current_user)],
    post_db: Annotated[Post, Depends(dependens_postdb_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await PostService().delete_post(
        session=session, post_db=post_db, current_user=current_user
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_posts_end_point(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> list[OutPost]:
    return await PostService().get_all_posts(session=session)


@router.get("/{post_id}/", response_model=OutPost)
async def get_by_id_post_end_point(
    post_db: Annotated[Post, Depends(dependens_postdb_by_id)],
) -> OutPost:
    return await PostService().get_by_id_post(post_db=post_db)


@router.put("/{post_id}/", response_model=OutPost)
async def update_post_end_point(
    post: UpdatePost,
    post_to_redact: Annotated[Post, Depends(dependens_check_post_and_user_correct)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> OutPost:
    return await PostService().update_post(session=session, post=post, post_to_redact=post_to_redact)
