from abc import ABC, abstractmethod

from app.core.models import User


class IUserRepository(ABC):

    @abstractmethod
    async def add_user (self, user:User)->User:
        pass

    @abstractmethod
    async def activate_user(self, user:User)->None:
        pass

    @abstractmethod
    async def get_user_by_username(self,username:str)->User | None:
        pass

    @abstractmethod
    async def get_user_by_email(self,email:str)->User | None:
        pass

    @abstractmethod
    async def get_user_by_id(self,id:int)->User | None:
        pass

    @abstractmethod
    async def delete_user(self,user:User)->None:
        pass

    @abstractmethod
    async def delete_all_users(self)->None:
        pass

    @abstractmethod
    async def delete_no_comfirm_users(self)->None:
        pass

    @abstractmethod
    async def add_refresh_token(self,user:User,refresh_toket:str)->None:
        pass
