from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import delete, select


from core.models import User
from .schemas import UserBase,Create_User


async def create_user(session:AsyncSession, user_create:Create_User):
    user=User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return  user


async def delete_user(session:AsyncSession, user:UserBase):
    await session.delete(user)
    await session.commit()

async def get_user(session:AsyncSession, user_id):
    return await session.get(User, user_id)

async def delete_users_all(session:AsyncSession):
    stat=select(User).order_by(User.id)
    result:Result=await session.execute(stat)
    users=result.scalars().all()
    for user in users:
        await session.delete(user)
    await session.commit()