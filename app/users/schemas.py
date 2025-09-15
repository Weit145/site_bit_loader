from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    usernmae:str
    pass

class Create_User(UserBase):
    pass

class User(UserBase):
    model_config=ConfigDict(from_attributes=True)
    id:int