from fastapi import APIRouter, Depends, status, HTTPException, Query

from pytest import Session
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated,List

from core.models.db_hellper import db_helper  
from core.models.post import Post
from core.models.user import User

from .schemas import CreatePost,PostBase,UpdatePost, PostResponse,OutPost
from . import crud
from app.users.schemas import UserResponse
from users.crud import get_current_user
from .dependens import post_by_id,post_id_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/",response_model=OutPost)
async def create_post(
    post:Annotated[PostBase,Query(mix_length=3)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->OutPost:
    cr_post = CreatePost(title=post.title,body=post.body,user_id=current_user.id)
    new_post= await crud.create_post(post_create=cr_post,session=session)
    return OutPost(title=new_post.title,body=new_post.body,user_name=current_user.username)

@router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_all(
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    return await crud.delete_all(session=session)
    
@router.delete("/{post_id}/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    post:Annotated[PostResponse, Depends(post_by_id)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->None:
    await crud.delete_by_id(session=session,post=post,user_id=current_user.id)

@router.get("/",status_code=status.HTTP_200_OK)
async def get_all(
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->List[PostResponse]:
    return await crud.get_all(session=session)

@router.get("/{post_id}/",response_model=OutPost)
async def get_by_id(
    post:Annotated[OutPost,Depends(post_id_user)]
)->OutPost:
    return post
    
@router.put("/{post_id}/",response_model=OutPost)
async def put_post(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    post:Annotated[UpdatePost,Query(mix_length=3)],
    posts:Annotated[PostResponse, Depends(post_by_id)],
    session:Annotated[AsyncSession, Depends(db_helper.session_dependency)]
)->OutPost:
    new_post=await crud.update_post(session=session,post=post,posts=posts,user_id=current_user.id)
    return OutPost(title=new_post.title,body=new_post.body,user_name=current_user.username)
