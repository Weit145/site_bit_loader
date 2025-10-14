from typing import Annotated

from core.models.db_hellper import db_helper
from core.models.post import Post
from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from users.dependens import Get_Current_User
from users.schemas import UserResponse

from . import crud
from .dependens import Check_Post_And_User_Correct, Postdb_By_Id
from .schemas import CreatePost, OutPost, UpdatePost

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=OutPost)
async def Create_Post_EndPoint(
    post: Annotated[CreatePost, Form()],
    current_user: Annotated[UserResponse, Depends(Get_Current_User)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> OutPost:
    return await crud.Create_Post(
        post_create=post, user_id=current_user.id, session=session
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def Dellete_All_Posts_EndPoint(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    return await crud.Dellete_All_Posts(session=session)


@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def Delete_Postdb_By_Id_EndPoint(
    current_user: Annotated[UserResponse, Depends(Get_Current_User)],
    post_db: Annotated[Post, Depends(Postdb_By_Id)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> None:
    await crud.Delete_Postdb_By_Id(
        session=session, post_db=post_db, username=current_user.username
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def Get_All_Posts_EndPoint(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> list[OutPost]:
    return await crud.Get_All_Posts(session=session)


@router.get("/{post_id}/", response_model=OutPost)
async def Get_By_Id_Post_EndPoint(
    post_db: Annotated[Post, Depends(Postdb_By_Id)],
) -> OutPost:
    return crud.Postdb_To_PostOut(post_db=post_db)


@router.put("/{post_id}/", response_model=OutPost)
async def Update_Post_EndPoint(
    post: Annotated[UpdatePost, Form()],
    post_to_redact: Annotated[Post, Depends(Check_Post_And_User_Correct)],
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
) -> OutPost:
    return await crud.Update_Post(
        session=session, post=post, post_to_redact=post_to_redact
    )
