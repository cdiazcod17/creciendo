from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.health_note import HealthNote
from app.models.baby import Baby
from .base import BaseRepository

class HealthNoteRepository(BaseRepository[HealthNote]):
    def __init__(self, session: Session):
        super().__init__(HealthNote, session)

    def get_by_id_and_baby_id(self, health_note_id: UUID, baby_id: UUID) -> HealthNote | None:
        return self.session.execute(
            select(HealthNote).where(
                HealthNote.id == health_note_id,
                HealthNote.baby_id == baby_id,
                HealthNote.deleted_at.is_(None),
            )
        ).scalar_one_or_none()

    def get_owned_by_id(self, user_id: UUID, health_note_id: UUID) -> HealthNote | None:
        return self.session.execute(
            select(HealthNote)
            .join(Baby, Baby.id == HealthNote.baby_id)
            .where(
                HealthNote.id == health_note_id,
                Baby.user_id == user_id,
                HealthNote.deleted_at.is_(None),
            )
        ).scalar_one_or_none()

    def list_by_baby_id_paginated(
        self,
        baby_id: UUID,
        *,
        limit: int,
        offset: int,
        note_type: str | None = None,
        title_contains: str | None = None,
        recorded_from: datetime | None = None,
        recorded_to: datetime | None = None,
    ) -> list[HealthNote]:
        stmt = select(HealthNote).where(
            HealthNote.baby_id == baby_id,
            HealthNote.deleted_at.is_(None),
        )

        if note_type:
            stmt = stmt.where(HealthNote.note_type == note_type.strip())

        if title_contains:
            stmt = stmt.where(HealthNote.title.ilike(f"%{title_contains.strip()}%"))

        if recorded_from:
            stmt = stmt.where(HealthNote.recorded_at >= recorded_from)

        if recorded_to:
            stmt = stmt.where(HealthNote.recorded_at <= recorded_to)

        stmt = (
            stmt.order_by(HealthNote.recorded_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return list(self.session.execute(stmt).scalars().all())
