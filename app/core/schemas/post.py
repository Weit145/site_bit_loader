from pydantic import BaseModel


class UpdatePost(BaseModel):
    title: str
    body: str
