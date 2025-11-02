from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Profile
from app.core.repositories.profile_repository import IProfileRepository


class SQLAlchemyProfileRepository(IProfileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_profile(self, user_id: int) -> None:
        profile_db = Profile(
            name_img = "default.png",
            img = False,
            user_id = user_id,
        )
        self.session.add(profile_db)
        await self.session.commit()
        await self.session.refresh(profile_db)

    async def update_profile(self, profile: Profile) -> Profile:
        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def reset_profile(self, profile: Profile) -> Profile:
        profile.name_img = "default.png"
        profile.img = False
        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def reset_all_profile(self) -> None:
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
