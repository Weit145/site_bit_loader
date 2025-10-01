from fastapi import APIRouter, Depends, status, HTTPException

from pytest import Session
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from core.models.db_hellper import db_helper  
from core.models.post import Post

from .schemas import CreatePost,PostBase,UpdatePost
from . import crud
from app.users.schemas import User
from users.crud import get_current_user
from .dependens import post_by_id

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/",response_model=CreatePost)
async def create_post(
    post:PostBase,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    cr_post = CreatePost(title=post.title,body=post.body,user_id=current_user.id)
    return await crud.create_post(post_create=cr_post,session=session)

@router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_all(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.delete_all(session=session)
    
@router.delete("/{post_id}/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    post:int = Depends(post_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.delete_by_id(session=session,post_id=post.id,user_id=current_user.id)

@router.get("/",status_code=status.HTTP_200_OK)
async def get_all(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_all(session=session)

@router.get("/{post_id}/",response_model=PostBase)
async def get_by_id(
    post:int = Depends(post_by_id),
):
    return post

@router.put("/{post_id}/",response_model=PostBase)
async def put_post(
    current_user: Annotated[User, Depends(get_current_user)],
    post:UpdatePost,
    posts:int = Depends(post_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency)
)->Post:
    return await crud.update_post(session=session,post=post,posts=posts,user_id=current_user.id)