from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import AppointmentStatus


class AppointmentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=2, max_length=120)
    scheduled_at: datetime
    status: AppointmentStatus = AppointmentStatus.scheduled
    provider_name: str | None = Field(default=None, max_length=120)
    location: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=1000)


class AppointmentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=2, max_length=120)
    scheduled_at: datetime | None = None
    status: AppointmentStatus | None = None
    provider_name: str | None = Field(default=None, max_length=120)
    location: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=1000)


class AppointmentRead(BaseModel):
    id: UUID
    baby_id: UUID
    title: str
    scheduled_at: datetime
    status: AppointmentStatus
    provider_name: str | None = None
    location: str | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)