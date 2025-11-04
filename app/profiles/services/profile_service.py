from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Profile
from app.core.services.profile_servicr import SQLAlchemyProfileRepository
from app.profiles.services.iprofile_service import IProfileService
from app.profiles.utils.convert import (
    convert_profiledb_to_out,
)
from app.profiles.utils.schemas import ProfileOut


class ProfileService(IProfileService):

    # Me
    async def read_me_profile(self, profile: Profile) -> ProfileOut:
        return convert_profiledb_to_out(profile)

    async def update_profile(self, session: AsyncSession, profile: Profile, new_profile: Profile) -> ProfileOut:
        await SQLAlchemyProfileRepository(session).update_profile(profile, new_profile)
        return convert_profiledb_to_out(new_profile)

    async def reset_me(self, session: AsyncSession, profile: Profile) -> ProfileOut:
        await SQLAlchemyProfileRepository(session).reset_profile(profile)


    # Admin
    async def reset_all_profiles(self, session: AsyncSession) -> None:
        await SQLAlchemyProfileRepository(session).reset_all_profiles()

    async def delete_all_profiles(self, session: AsyncSession) -> None:
        await SQLAlchemyProfileRepository(session).delete_all_profiles()
