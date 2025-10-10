from .base import Base
from enum import unique
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship



if TYPE_CHECKING:
    from .user import User

class Post(Base):
    __tablename__="Post"
    title: Mapped[str]= mapped_column(
        String(100), 
        unique=False,
        nullable=False
    )
    body: Mapped[str]=mapped_column(
        Text,
        default="",
        server_default=""
    )

    user_id:Mapped[int]=mapped_column(ForeignKey("User.id"))
    user:Mapped["User"] = relationship(
        back_populates="posts",
        lazy="joined"
    )