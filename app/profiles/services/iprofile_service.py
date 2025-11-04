from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Profile
from app.profiles.utils.schemas import ProfileResponse


class IProfileService(ABC):

    # Me
    @abstractmethod
    async def read_me_profile(self, profile: Profile) -> ProfileResponse:
        pass

    @abstractmethod
    async def update_profile(self, session: AsyncSession, profile: Profile, new_profile: Profile) -> ProfileResponse:
        pass

    @abstractmethod
    async def reset_me(self, session: AsyncSession, profile: Profile) -> None:
        pass


    # Admin
    @abstractmethod
    async def reset_all_profiles(self, session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def delete_all_profiles(self, session: AsyncSession) -> None:
        pass
