from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.baby import Baby
from app.models.health_note import HealthNote
from app.models.user import User
from app.schemas.health_note import HealthNoteCreate, HealthNoteUpdate


class HealthNoteService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def resolve_target_baby(self, user: User, baby_id: UUID | None) -> Baby:
        target_baby_id = baby_id or user.active_baby_id

        if target_baby_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No hay bebé activo y no se envió baby_id.",
            )

        baby = self.db.execute(
            select(Baby).where(
                Baby.id == target_baby_id,
                Baby.user_id == user.id,
            )
        ).scalar_one_or_none()

        if baby is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bebé no encontrado.",
            )

        return baby

    def get_owned_health_note(self, user: User, health_note_id: UUID) -> HealthNote:
        health_note = self.db.execute(
            select(HealthNote)
            .join(Baby, Baby.id == HealthNote.baby_id)
            .where(
                HealthNote.id == health_note_id,
                Baby.user_id == user.id,
                HealthNote.deleted_at.is_(None),
            )
        ).scalar_one_or_none()

        if health_note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota de salud no encontrada.",
            )

        return health_note

    def list_health_notes(
        self,
        user: User,
        baby_id: UUID | None,
        *,
        limit: int,
        offset: int,
        note_type: str | None,
        title_contains: str | None,
        recorded_from: datetime | None,
        recorded_to: datetime | None,
    ) -> list[HealthNote]:
        baby = self.resolve_target_baby(user, baby_id)

        stmt = select(HealthNote).where(
            HealthNote.baby_id == baby.id,
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

        return list(self.db.execute(stmt).scalars().all())

    def create_health_note(self, user: User, payload: HealthNoteCreate) -> HealthNote:
        baby = self.resolve_target_baby(user, payload.baby_id)

        health_note = HealthNote(
            baby_id=baby.id,
            note_type=payload.note_type.strip(),
            title=payload.title.strip(),
            content=payload.content.strip(),
            recorded_at=payload.recorded_at,
        )

        self.db.add(health_note)
        self.db.commit()
        self.db.refresh(health_note)

        return health_note

    def get_health_note(self, user: User, health_note_id: UUID) -> HealthNote:
        return self.get_owned_health_note(user, health_note_id)

    def update_health_note(
        self,
        user: User,
        health_note_id: UUID,
        payload: HealthNoteUpdate,
    ) -> HealthNote:
        health_note = self.get_owned_health_note(user, health_note_id)
        update_data = payload.model_dump(exclude_unset=True)

        for field_name, value in update_data.items():
            if field_name in {"note_type", "title", "content"} and value is not None:
                value = value.strip()

            setattr(health_note, field_name, value)

        self.db.add(health_note)
        self.db.commit()
        self.db.refresh(health_note)

        return health_note

    def delete_health_note(self, user: User, health_note_id: UUID) -> None:
        health_note = self.get_owned_health_note(user, health_note_id)

        health_note.deleted_at = datetime.now(timezone.utc)
        self.db.add(health_note)
        self.db.commit()