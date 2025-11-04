from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Profile
from app.core.repositories.profile_repository import IProfileRepository


class SQLAlchemyProfileRepository(IProfileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_profile(self, profile: Profile) -> Profile:
        updated_profile = await self.session.merge(profile)
        await self.session.commit()
        await self.session.refresh(updated_profile)
        return updated_profile

    async def reset_profile(self, profile: Profile) -> Profile:
        profile.name_img = "default.png"
        profile.img = False
        await self.session.add(profile)
        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def reset_all_profiles(self) -> None:
        stm = select(Profile).where(Profile.img == 1)
        result = await self.session.execute(stm)
        profile_db = list(result.scalars().all())
        for profile in profile_db:
            await self.reset_profile(profile=profile)

    async def delete_all_profiles(self) -> None:
        stmt = select(Profile).order_by(Profile.id)
        result = await self.session.execute(stmt)
        profiles = result.scalars().all()
        for profile in profiles:
            await self.session.delete(profile)
        await self.session.commit()

    async def get_profile(self, profile_id: int) -> Profile | None:
        return await self.session.get(Profile, profile_id)

    async def get_profile_by_user_id(self, user_id: int) -> Profile | None:
        return await self.session.execute(select(Profile).where(Profile.user_id == user_id))
