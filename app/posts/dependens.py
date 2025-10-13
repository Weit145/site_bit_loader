from typing import Annotated

from core.models import Post, db_helper
from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from users.dependens import Get_Current_User
from users.schemas import UserResponse


async def Postdb_By_Id(
    post_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Post:
    post_db = await session.get(Post, post_id)
    if post_db is not None:
        return post_db
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found"
    )


def Check_Post_And_User_Correct(
    post_to_redact: Annotated[Post, Depends(Postdb_By_Id)],
    current_user: Annotated[UserResponse, Depends(Get_Current_User)],
) -> Post:
    if (not post_to_redact) or (post_to_redact.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return post_to_redact
