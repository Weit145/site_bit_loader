from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: Annotated[str, MinLen(4), MaxLen(32)]


class UserCreate(UserBase):
    password: Annotated[str, MinLen(6), MaxLen(32)]


class UserLogin(UserBase):
    password: Annotated[str, MinLen(6), MaxLen(32)]


class UserGet(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AvtorUser(UserBase):
    disabled: bool | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
