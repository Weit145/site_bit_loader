from enum import unique

from typing import TYPE_CHECKING

from sqlalchemy import String,Boolean
from sqlalchemy.orm import Mapped, mapped_column,relationship

from .base import Base


if TYPE_CHECKING:
    from .post import Post
class User(Base):

    __tablename__="User"

    username:Mapped[str]=mapped_column(String(32),unique=True, index=True)


    password:Mapped[str]=mapped_column(String,unique=False)

    disabled: Mapped[bool] = mapped_column(Boolean, default=False)

    posts:Mapped[list["Post"]]=relationship(back_populates="user")