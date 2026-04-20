from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HealthNoteCreate(BaseModel):
    baby_id: UUID | None = None
    note_type: str = Field(min_length=1, max_length=60)
    title: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=1, max_length=5000)
    recorded_at: datetime


class HealthNoteUpdate(BaseModel):
    note_type: str | None = Field(default=None, min_length=1, max_length=60)
    title: str | None = Field(default=None, min_length=1, max_length=120)
    content: str | None = Field(default=None, min_length=1, max_length=5000)
    recorded_at: datetime | None = None


class HealthNoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    baby_id: UUID
    note_type: str
    title: str
    content: str
    recorded_at: datetime
    created_at: datetime
    updated_at: datetime
