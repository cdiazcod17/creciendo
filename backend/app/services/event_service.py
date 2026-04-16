from uuid import UUID

from fastapi import HTTPException, status
from app.schemas.event import EventCreate, EventUpdate

from app.models.baby import Baby
from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventCreate
from app.services.base import BaseService


class EventService(BaseService):
    def _get_owned_baby(self, baby_id: UUID, current_user: User) -> Baby:
        baby = (
            self.session.query(Baby)
            .filter(
                Baby.id == baby_id,
                Baby.user_id == current_user.id,
            )
            .first()
        )

        if not baby:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bebé no encontrado",
            )

        return baby

    def _get_event_in_baby(self, baby_id: UUID, event_id: UUID, current_user: User) -> Event:
        self._get_owned_baby(baby_id, current_user)

        event = (
            self.session.query(Event)
            .filter(
                Event.id == event_id,
                Event.baby_id == baby_id,
            )
            .first()
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado",
            )

        return event

    def create_event(self, baby_id: UUID, payload: EventCreate, current_user: User) -> Event:
        self._get_owned_baby(baby_id, current_user)

        event = Event(
            baby_id=baby_id,
            event_type=payload.event_type,
            occurred_at=payload.occurred_at,
            amount=payload.amount,
            notes=payload.notes,
        )

        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def list_events(self, baby_id: UUID, current_user: User) -> list[Event]:
        self._get_owned_baby(baby_id, current_user)

        return (
            self.session.query(Event)
            .filter(Event.baby_id == baby_id)
            .order_by(Event.occurred_at.desc())
            .all()
        )

    def get_event_by_id(self, baby_id: UUID, event_id: UUID, current_user: User) -> Event:
        return self._get_event_in_baby(baby_id, event_id, current_user)
    
    def update_event(self, baby_id: UUID, event_id: UUID, payload: EventUpdate, current_user: User) -> Event:
        event = self._get_event_in_baby(baby_id, event_id, current_user)

        update_data = payload.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se enviaron campos para actualizar",
            )

        for field, value in update_data.items():
            setattr(event, field, value)

        self.session.commit()
        self.session.refresh(event)
        return event

    def delete_event(self, baby_id: UUID, event_id: UUID, current_user: User) -> None:
        event = self._get_event_in_baby(baby_id, event_id, current_user)

        self.session.delete(event)
        self.session.commit()