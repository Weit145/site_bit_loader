from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile


class User(Base):
    __tablename__ = "User"

    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)

    password: Mapped[str] = mapped_column(String, unique=False)

    email: Mapped[str] = mapped_column(String,  unique=True)

    active: Mapped[bool] = mapped_column(Boolean, server_default=text("0"))

    refresh_token: Mapped[str] = mapped_column(String, server_default=text("0"))

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    profile: Mapped["Profile"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="joined",
    )
