from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, String, Text, Uuid, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import BabySex
from app.db.base import TimestampedUUIDModel


class Baby(TimestampedUUIDModel):
    __tablename__ = "babies"

    name: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
    )

    birth_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    sex: Mapped[BabySex | None] = mapped_column(
        SQLEnum(BabySex, name="baby_sex"),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    photo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="babies",
    )

    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="baby",
        cascade="all, delete-orphan",
    )

    growth_records: Mapped[list["GrowthRecord"]] = relationship(
        "GrowthRecord",
        back_populates="baby",
        cascade="all, delete-orphan",
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="baby",
        cascade="all, delete-orphan",
    )