from abc import ABC, abstractmethod
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi import Path
from app.core.models import User

from app.users.schemas import (
    Token,
    UserLogin,
    UserResponse,
)


class IUserService(ABC):

    # Registration
    @abstractmethod
    async def create_user(self,session:AsyncSession, user:User)->None:
        pass

    @abstractmethod
    async def registration_confirmation(self, session:AsyncSession,token:str)->JSONResponse:
        pass


    # Auth
    @abstractmethod
    async def refresh_token(self,session:AsyncSession,refresh_token:str)->Token:
        pass

    @abstractmethod
    async def login_for_access(self,user:UserLogin,session:AsyncSession)->JSONResponse:
        pass


    # Me
    @abstractmethod
    async def delete_me_user(self,current_user:UserResponse,session:AsyncSession)->None:
        pass

    @abstractmethod
    async def read_me_user(self, current_user:UserResponse)->UserResponse:
        pass


    # Admin
    @abstractmethod
    async def delete_all_users(self, session:AsyncSession)->None:
        pass

    @abstractmethod
    async def dellete_all_no_comfirm_users(self, session:AsyncSession)->None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: Annotated[int, Path(ge=1)],)->UserResponse:
        pass