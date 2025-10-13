from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Profile(Base):
    __tablename__ = "Profile"
    name_img: Mapped[str] = mapped_column(String(100), nullable=False)
    img: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="profile", single_parent=True)
