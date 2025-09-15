from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import User,   Create_User

async def user_by_id(user_id:Annotated[int,Path],session:AsyncSession = Depends(db_helper.session_dependency)):
    product=await crud.get_user(session=session,user_id=user_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product  {user_id} not found"
    )