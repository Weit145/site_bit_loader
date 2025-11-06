from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Profile
from app.core.services.profile_servicr import SQLAlchemyProfileRepository
from app.core.security.file import (
    clear_upload_dir,
    delete_uploaded_file
)
from app.profiles.services.iprofile_service import IProfileService
from app.profiles.utils.convert import (
    convert_profiledb_to_out,
)
from app.profiles.utils.schemas import ProfileOut


class ProfileService(IProfileService):
    
    def __init__(self):
        old_img = ""

    # Me
    async def read_me_profile(self, profile: Profile) -> ProfileOut:
        return convert_profiledb_to_out(profile)

    async def update_profile(self, session: AsyncSession, new_profile: Profile, profile:Profile) -> ProfileOut:
        self.old_img = profile.name_img 
        await SQLAlchemyProfileRepository(session).update_profile(new_profile,profile)
        delete_uploaded_file(self.old_img)
        return convert_profiledb_to_out(profile)

    async def reset_me(self, session: AsyncSession, profile: Profile) -> ProfileOut:
        self.old_img = profile.name_img 
        await SQLAlchemyProfileRepository(session).reset_profile(profile)
        delete_uploaded_file(self.old_img)
        return convert_profiledb_to_out(profile)

    # Admin
    async def reset_all_profiles(self, session: AsyncSession) -> None:
        await SQLAlchemyProfileRepository(session).reset_all_profiles()
        clear_upload_dir()

    async def delete_all_profiles(self, session: AsyncSession) -> None:
        await SQLAlchemyProfileRepository(session).delete_all_profiles()
        clear_upload_dir()
