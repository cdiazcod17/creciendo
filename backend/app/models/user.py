# app/models/user.py
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import Roles
from app.db.base import TimestampedUUIDModel

if TYPE_CHECKING:
    from app.models.baby import Baby


class User(TimestampedUUIDModel):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[Roles] = mapped_column(
        SQLEnum(Roles, name="roles"),
        default=Roles.user,
        nullable=False,
    )

    token_version: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    active_baby_id: Mapped[str | None] = mapped_column(
        ForeignKey("babies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    babies: Mapped[list["Baby"]] = relationship(
        "Baby",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="Baby.user_id",
    )

    active_baby: Mapped["Baby | None"] = relationship(
        "Baby",
        foreign_keys=[active_baby_id],
        uselist=False,
        post_update=True,
    )