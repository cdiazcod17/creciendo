from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, Text, Uuid, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import EventType
from app.db.base import TimestampedUUIDModel


class Event(TimestampedUUIDModel):
    __tablename__ = "events"

    baby_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("babies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(EventType, name="event_types"),
        nullable=False,
        index=True,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    amount: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    baby: Mapped["Baby"] = relationship(
        "Baby",
        back_populates="events",
    )