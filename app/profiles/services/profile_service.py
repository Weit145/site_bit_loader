from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Profile
from app.core.services.profile_servicr import SQLAlchemyProfileRepository
from app.profiles.schemas import ProfileResponse
from app.profiles.services.iprofile_service import IProfileService
from app.profiles.utils.checks import check_no_profile_in_db
from app.profiles.utils.convert import convert_profiledb


class ProfileService(IProfileService):

    async def create_profile(self, session: AsyncSession, user_id: int) -> None:
        profile = await SQLAlchemyProfileRepository(session).get_profile(user_id)
        check_no_profile_in_db(profile)
        await SQLAlchemyProfileRepository(session).create_profile(user_id)


    # Me
    async def read_me_profile(self, profile: Profile) -> ProfileResponse:
        return convert_profiledb(profile)

    async def update_profile(self, session: AsyncSession, profile: Profile, new_profile: Profile) -> ProfileResponse:
        await SQLAlchemyProfileRepository(session).update_profile(profile, new_profile)
        return convert_profiledb(new_profile)

    async def reset_me(self, session: AsyncSession, profile: Profile) -> None:
        await SQLAlchemyProfileRepository(session).reset_profile(profile)


    # Admin
    async def reset_all_profiles(self, session: AsyncSession) -> None:
        await SQLAlchemyProfileRepository(session).reset_all_profiles()

    async def delete_all_profiles(self, session: AsyncSession) -> None:
        await SQLAlchemyProfileRepository(session).delete_all_profiles()
