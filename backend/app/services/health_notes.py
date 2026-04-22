from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.health_note import HealthNote
from app.schemas.health_note import HealthNoteCreate, HealthNoteUpdate
from app.services.base import BaseService
from app.repositories.health_note_repository import HealthNoteRepository

class HealthNoteService(BaseService):
    def __init__(self, session: Session, health_note_repo: HealthNoteRepository):
        super().__init__(session)
        self.health_note_repo = health_note_repo

    def _get_health_note_in_baby(self, baby_id: UUID, health_note_id: UUID) -> HealthNote:
        health_note = self.health_note_repo.get_by_id_and_baby_id(health_note_id, baby_id)
        # Note: HealthNoteRepository needs get_by_id_and_baby_id if we want consistency
        # Let me check what I implemented in HealthNoteRepository
        return health_note

    def list_health_notes(
        self,
        baby_id: UUID,
        *,
        limit: int,
        offset: int,
        note_type: str | None,
        title_contains: str | None,
        recorded_from: datetime | None,
        recorded_to: datetime | None,
    ) -> list[HealthNote]:
        return self.health_note_repo.list_by_baby_id_paginated(
            baby_id=baby_id,
            limit=limit,
            offset=offset,
            note_type=note_type,
            title_contains=title_contains,
            recorded_from=recorded_from,
            recorded_to=recorded_to,
        )

    def create_health_note(self, payload: HealthNoteCreate) -> HealthNote:
        health_note = HealthNote(
            baby_id=payload.baby_id,
            note_type=payload.note_type.strip(),
            title=payload.title.strip(),
            content=payload.content.strip(),
            recorded_at=payload.recorded_at,
        )
        return self.health_note_repo.add(health_note)

    def get_health_note(self, baby_id: UUID, health_note_id: UUID) -> HealthNote:
        note = self.health_note_repo.get_by_id_and_baby_id(health_note_id, baby_id)
        if not note:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota de salud no encontrada.",
            )
        return note

    def update_health_note(
        self,
        baby_id: UUID,
        health_note_id: UUID,
        payload: HealthNoteUpdate,
    ) -> HealthNote:
        health_note = self.get_health_note(baby_id, health_note_id)
        update_data = payload.model_dump(exclude_unset=True)

        for field_name, value in update_data.items():
            if field_name in {"note_type", "title", "content"} and value is not None:
                value = value.strip()
            setattr(health_note, field_name, value)

        self.health_note_repo.update()
        return health_note

    def delete_health_note(self, baby_id: UUID, health_note_id: UUID) -> None:
        health_note = self.get_health_note(baby_id, health_note_id)
        health_note.deleted_at = datetime.now(timezone.utc)
        self.health_note_repo.update()
