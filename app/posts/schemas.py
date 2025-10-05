from typing import Annotated
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title:str
    body:str


class CreatePost(PostBase):
    user_id:int
    pass

class СorrectPost(PostBase):
    user_id:int
    pass

class UpdatePost(PostBase):
    pass

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int