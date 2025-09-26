from typing import Annotated
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title:str
    body:str
    user_id:int

class CreatePost(PostBase):
    pass

class User(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int