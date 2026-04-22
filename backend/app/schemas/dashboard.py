from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.core.enums import EventType


class DashboardLastEvent(BaseModel):
    id: UUID
    event_type: EventType
    occurred_at: datetime
    amount: int | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DashboardBabyItem(BaseModel):
    id: UUID
    name: str
    last_event: DashboardLastEvent | None = None

    model_config = ConfigDict(from_attributes=True)


class DashboardRecentEvent(BaseModel):
    id: UUID
    baby_id: UUID
    baby_name: str
    event_type: EventType
    occurred_at: datetime
    amount: int | None = None
    notes: str | None = None


class DashboardSummary(BaseModel):
    user_id: UUID
    full_name: str
    total_babies: int
    total_events: int
    babies: list[DashboardBabyItem]
    recent_events: list[DashboardRecentEvent]