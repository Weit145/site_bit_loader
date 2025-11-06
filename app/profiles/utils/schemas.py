from pydantic import BaseModel, ConfigDict


class ProfileBase(BaseModel):
    name_img: str
    img: bool


class ProfileResponse(ProfileBase):
    user_id: int
    id: int

class ProfileOut(ProfileBase):
    username: str
    user_id: int
