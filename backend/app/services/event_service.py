from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate
from app.services.base import BaseService
from app.repositories.event_repository import EventRepository
from app.core.enums import EventType

class EventService(BaseService):
    def __init__(self, session: Session, event_repo: EventRepository):
        super().__init__(session)
        self.event_repo = event_repo

    def _get_event_in_baby(self, baby_id: UUID, event_id: UUID) -> Event:
        event = self.event_repo.get_by_id_and_baby_id(event_id, baby_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado",
            )
        return event

    def create_event(self, baby_id: UUID, payload: EventCreate) -> Event:
        event = Event(
            baby_id=baby_id,
            event_type=payload.event_type,
            occurred_at=payload.occurred_at,
            amount=payload.amount,
            notes=payload.notes,
        )
        return self.event_repo.add(event)

    def list_events(
        self, 
        baby_id: UUID, 
        event_type: EventType | None = None,
        limit: int = 20,
        offset: int = 0
    ) -> list[Event]:
        return self.event_repo.list_by_baby_id(baby_id, event_type, limit, offset)

    def get_event_by_id(self, baby_id: UUID, event_id: UUID) -> Event:
        return self._get_event_in_baby(baby_id, event_id)
    
    def update_event(self, baby_id: UUID, event_id: UUID, payload: EventUpdate) -> Event:
        event = self._get_event_in_baby(baby_id, event_id)
        update_data = payload.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se enviaron campos para actualizar",
            )

        for field, value in update_data.items():
            setattr(event, field, value)

        self.event_repo.update()
        return event

    def delete_event(self, baby_id: UUID, event_id: UUID) -> None:
        event = self._get_event_in_baby(baby_id, event_id)
        self.event_repo.delete(event)
