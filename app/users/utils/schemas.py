from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: Annotated[str, MinLen(4), MaxLen(32)]


class UserCreate(UserBase):
    password: Annotated[str, MinLen(6), MaxLen(32)]
    email: Annotated[EmailStr,MinLen(6)]


class UserLogin(UserBase):
    password: Annotated[str, MinLen(6), MaxLen(32)]


class UserGet(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    email:str
    id: int


class AvtorUser(UserBase):
    active: bool | None = None

class OutUser(UserBase):
    email: str
    id: int
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

