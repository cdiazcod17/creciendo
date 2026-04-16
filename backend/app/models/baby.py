from datetime import date
import uuid
from sqlalchemy import String, Text, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import TimestampedUUIDModel
from app.core.enums import BabySex


class Baby(TimestampedUUIDModel):
    __tablename__ = "babies"

    name: Mapped[str] = mapped_column(String(250), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    sex: Mapped[BabySex | None] = mapped_column(
        SQLEnum(BabySex, name="baby_sex"), 
        nullable=True
    )
    
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    
    user: Mapped["User"] = relationship("User", back_populates="babies")
    
    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="baby",
        cascade="all, delete-orphan"
    )   
    growth_records: Mapped[list["GrowthRecord"]] = relationship(
        "GrowthRecord",
        back_populates="baby",
        cascade="all, delete-orphan"
    )
    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="baby",
        cascade="all, delete-orphan"
    )