from fastapi import APIRouter, Depends,HTTPException, status

from core.models import db_hellper

from .schemas import Create_User, UserBase, User
from core.models.db_hellper import db_helper
from . import crud
from .dependens import user_by_id

from sqlalchemy.ext.asyncio import AsyncSession

router=APIRouter(tags=["Users"])

@router.post("/",response_model=User)
async def create_user(user_in:Create_User,session:AsyncSession=Depends(db_helper.session_dependency)):
    return await crud.create_user(session=session,user_create=user_in)

@router.delete("/{user_id}/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user:UserBase= Depends(user_by_id),session:AsyncSession=Depends(db_helper.session_dependency)):
    await crud.delete_user(session=session,user=user)

@router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_all(session:AsyncSession=Depends(db_helper.session_dependency)):
    await crud.delete_users_all(session=session)


@router.get("/{user_id}/",response_model=User)
async def get_user(user:UserBase= Depends(user_by_id)):
    return user