from pydantic import BaseModel, ConfigDict


class ProfileBase(BaseModel):
    name_img: str
    img: bool


class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    id: int
