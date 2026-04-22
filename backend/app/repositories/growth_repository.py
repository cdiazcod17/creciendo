from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.growth_record import GrowthRecord
from .base import BaseRepository

class GrowthRepository(BaseRepository[GrowthRecord]):
    def __init__(self, session: Session):
        super().__init__(GrowthRecord, session)

    def list_by_baby_id(self, baby_id: UUID) -> list[GrowthRecord]:
        return list(
            self.session.execute(
                select(GrowthRecord)
                .where(GrowthRecord.baby_id == baby_id)
                .order_by(GrowthRecord.measured_at.desc())
            ).scalars().all()
        )

    def get_by_id_and_baby_id(self, growth_id: UUID, baby_id: UUID) -> GrowthRecord | None:
        return self.session.execute(
            select(GrowthRecord).where(
                GrowthRecord.id == growth_id,
                GrowthRecord.baby_id == baby_id
            )
        ).scalar_one_or_none()
