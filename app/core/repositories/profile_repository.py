from abc import ABC, abstractmethod

from app.core.models import Profile


class IProfileRepository(ABC):

    @abstractmethod
    async def create_profile(self, profile: Profile) -> None:
        pass

    @abstractmethod
    async def update_profile(self, profile: Profile) -> Profile:
        pass

    @abstractmethod
    async def reset_profile(self,  profile: Profile) -> Profile:
        pass

    @abstractmethod
    async def reset_all_profile(self) -> None:
        pass

    @abstractmethod
    async def delete_all_profiles(self) -> None:
        pass

    @abstractmethod
    async def get_profile(self, profile_id: int) -> Profile | None:
        pass
