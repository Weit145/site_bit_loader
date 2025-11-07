from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Profile
from app.profiles.utils.schemas import ProfileOut


class IProfileService(ABC):

    # Me
    @abstractmethod
    async def read_me_profile(self, profile: Profile) -> ProfileOut:
        pass

    @abstractmethod
    async def update_profile(self, session: AsyncSession, new_profile: Profile, profile: Profile) -> ProfileOut:
        pass

    @abstractmethod
    async def reset_me(self, session: AsyncSession, profile: Profile) -> ProfileOut:
        pass


    # Admin
    @abstractmethod
    async def reset_all_profiles(self, session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def delete_all_profiles(self, session: AsyncSession) -> None:
        pass
