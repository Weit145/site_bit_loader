from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.repositories.user_repository import IUserRepository


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self,  session:AsyncSession):
        self.session=session

    async def add_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def activate_user(self, user: User) -> None:
        user.active=True
        await self.session.commit()

    async def get_user_by_username(self, username: str) -> User | None:
        stmt  = select(User).where(User.username==username)
        result = await self.session.execute(stmt)
        user_db = result.scalar_one_or_none()
        return user_db

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email==email)
        result = await self.session.execute(stmt)
        user_db = result.scalar_one_or_none()
        return user_db

    async def get_user_by_id(self, id: int) -> User | None:
        user_db = await self.session.get(User,id)
        return user_db

    async def delete_user(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()

    async def delete_all_users(self) -> None:
        stmt = select(User).order_by(User.id)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        for user in users:
            await self.session.delete(user)
        await self.session.commit()

    async def delete_no_comfirm_users(self) -> None:
        stm = select(User).where(User.active==0)
        result = await self.session.execute(stm)
        users_db = list (result.scalars().all())
        for user in users_db:
            await self.session.delete(user)
        await self.session.commit()

    async def add_refresh_token(self,user:User, refresh_toket: str) -> None:
        user.refresh_token=refresh_toket
        user.active = True
        await self.session.commit()
        await self.session.refresh(user)
