from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, Uuid, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AppointmentStatus
from app.db.base import TimestampedUUIDModel


class Appointment(TimestampedUUIDModel):
    __tablename__ = "appointments"
    __table_args__ = (
        Index("ix_appointments_baby_id_scheduled_at", "baby_id", "scheduled_at"),
    )

    baby_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("babies.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[AppointmentStatus] = mapped_column(
        SQLEnum(AppointmentStatus, name="appointment_statuses"),
        nullable=False,
        default=AppointmentStatus.scheduled,
    )

    provider_name: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    baby: Mapped["Baby"] = relationship(
        "Baby",
        back_populates="appointments",
    )