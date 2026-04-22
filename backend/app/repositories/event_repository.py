from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.event import Event
from app.models.baby import Baby
from app.core.enums import EventType
from .base import BaseRepository

class EventRepository(BaseRepository[Event]):
    def __init__(self, session: Session):
        super().__init__(Event, session)

    def list_by_baby_id(
        self, 
        baby_id: UUID, 
        event_type: EventType | None = None,
        limit: int = 20,
        offset: int = 0
    ) -> list[Event]:
        stmt = select(Event).where(Event.baby_id == baby_id)
        
        if event_type:
            stmt = stmt.where(Event.event_type == event_type)
            
        stmt = stmt.order_by(Event.occurred_at.desc()).offset(offset).limit(limit)
        
        return list(self.session.execute(stmt).scalars().all())

    def get_by_id_and_baby_id(self, event_id: UUID, baby_id: UUID) -> Event | None:
        return self.session.execute(
            select(Event).where(
                Event.id == event_id,
                Event.baby_id == baby_id
            )
        ).scalar_one_or_none()

    def get_latest_by_baby_id(self, baby_id: UUID) -> Event | None:
        return self.session.execute(
            select(Event)
            .where(Event.baby_id == baby_id)
            .order_by(Event.occurred_at.desc())
            .limit(1)
        ).scalar_one_or_none()

    def count_by_baby_ids(self, baby_ids: list[UUID]) -> int:
        if not baby_ids:
            return 0
        return self.session.execute(
            select(func.count(Event.id)).where(Event.baby_id.in_(baby_ids))
        ).scalar_one()

    def list_recent_with_baby_name_by_user_id(self, user_id: UUID, limit: int = 5) -> list[tuple[Event, str]]:
        return list(
            self.session.execute(
                select(Event, Baby.full_name.label("baby_name"))
                .join(Baby, Event.baby_id == Baby.id)
                .where(Baby.user_id == user_id)
                .order_by(Event.occurred_at.desc())
                .limit(limit)
            ).all()
        )
