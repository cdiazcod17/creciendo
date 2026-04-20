# app/models/health_note.py
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import SoftDeleteTimestampedUUIDModel

if TYPE_CHECKING:
    from app.models.baby import Baby


class HealthNote(SoftDeleteTimestampedUUIDModel):
    __tablename__ = "health_notes"
    __table_args__ = (
        Index("ix_health_notes_baby_id_recorded_at", "baby_id", "recorded_at"),
    )

    baby_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("babies.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    note_type: Mapped[str] = mapped_column(String(60), nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    baby: Mapped["Baby"] = relationship(
        "Baby",
        back_populates="health_notes",
    )