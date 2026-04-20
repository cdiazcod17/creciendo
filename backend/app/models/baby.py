# app/models/baby.py
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Date, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import TimestampedUUIDModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.appointment import Appointment
    from app.models.event import Event
    from app.models.growth_record import GrowthRecord
    from app.models.health_note import HealthNote


class Baby(TimestampedUUIDModel):
    __tablename__ = "babies"

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    birth_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    sex: Mapped[str | None] = mapped_column(
        String(20),
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

    user: Mapped["User"] = relationship(
        "User",
        back_populates="babies",
        foreign_keys=[user_id],
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="baby",
        cascade="all, delete-orphan",
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

    health_notes: Mapped[list["HealthNote"]] = relationship(
        "HealthNote",
        back_populates="baby",
        cascade="all, delete-orphan",
    )