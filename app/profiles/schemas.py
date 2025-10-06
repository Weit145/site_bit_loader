from pydantic import BaseModel, ConfigDict

class ProfileBase(BaseModel):
    name_img:str
    img:bool

class CreateProfile(ProfileBase):
    user_id:int
    pass


class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)
    user_id:int
    id: int