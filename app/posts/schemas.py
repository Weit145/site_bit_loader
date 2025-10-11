from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title:str
    body:str


class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class OutPost(PostBase):
    name_img:str
    user_name:str
    id: int
    
class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    user_id:int
    id: int