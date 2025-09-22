from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict
from typing import Annotated

class UserBase(BaseModel):
    username: Annotated[str, MinLen(4), MaxLen(32)]

class AvtorUser(UserBase):
    disabled: bool | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class Create_User(UserBase):
    password: Annotated[str, MinLen(6), MaxLen(32)]  # Исправлено имя поля

class Enter_User(UserBase):
    password: Annotated[str, MinLen(6), MaxLen(32)]
    pod_password: Annotated[str, MinLen(6), MaxLen(32)]

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int