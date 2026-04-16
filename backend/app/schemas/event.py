from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import EventType


class EventCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    event_type: EventType
    occurred_at: datetime
    amount: int | None = Field(default=None, ge=0)
    notes: str | None = Field(default=None, max_length=500)


class EventUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    event_type: EventType | None = None
    occurred_at: datetime | None = None
    amount: int | None = Field(default=None, ge=0)
    notes: str | None = Field(default=None, max_length=500)


class EventRead(BaseModel):
    id: UUID
    baby_id: UUID
    event_type: EventType
    occurred_at: datetime
    amount: int | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)