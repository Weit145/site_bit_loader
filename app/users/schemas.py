from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict

from typing import Annotated

class UserBase(BaseModel):
    usernmae:Annotated[str,MinLen(4),MaxLen(32)]
    pass

class Create_User(UserBase):
    password:Annotated[str,MaxLen(6),MaxLen(32)]
    pass
class Enter_User(Create_User):
    pod_password:Annotated[str,MaxLen(6),MaxLen(32)]
    pass
class User(UserBase):
    model_config=ConfigDict(from_attributes=True)
    id:int