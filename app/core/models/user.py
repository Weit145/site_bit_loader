from enum import unique

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column,relationship

from .base import Base


if TYPE_CHECKING:
    from .post import Post
class User(Base):

    __tablename__="User"

    username:Mapped[str]=mapped_column(String(32),unique=False)


    password:Mapped[str]=mapped_column(String(32),unique=False)

    posts:Mapped[list["Post"]]=relationship(back_populates="user")