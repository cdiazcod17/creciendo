from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.baby import Baby
from .base import BaseRepository

class BabyRepository(BaseRepository[Baby]):
    def __init__(self, session: Session):
        super().__init__(Baby, session)

    def list_by_user_id(self, user_id: UUID) -> list[Baby]:
        return list(
            self.session.execute(
                select(Baby)
                .where(Baby.user_id == user_id)
                .order_by(Baby.created_at.desc())
            ).scalars().all()
        )

    def get_by_id_and_user_id(self, baby_id: UUID, user_id: UUID) -> Baby | None:
        return self.session.execute(
            select(Baby).where(
                Baby.id == baby_id,
                Baby.user_id == user_id
            )
        ).scalar_one_or_none()
