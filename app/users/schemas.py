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


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class Cookie(BaseModel):
    key:str
    value:str
    httponly:bool = False
    secure: bool = True
    samesite:str = "strict"
    max_age :int = 7*24*3600


# response.set_cookie(
#     key="refresh_token",
#     value=refresh_token,
#     httponly=True,    # 🔒 нельзя прочитать из JS
#     secure=True,      # 🚫 не уходит по HTTP, только HTTPS
#     samesite="Strict",# 🛡️ не отправляется с других сайтов (CSRF защита)
#     max_age=7 * 24 * 3600
# )
