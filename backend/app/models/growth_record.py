from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import TimestampedUUIDModel


class GrowthRecord(TimestampedUUIDModel):
    __tablename__ = "growth_records"

    baby_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("babies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    measured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    weight_kg: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    height_cm: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    head_circumference_cm: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    baby: Mapped["Baby"] = relationship(
        "Baby",
        back_populates="growth_records",
    )