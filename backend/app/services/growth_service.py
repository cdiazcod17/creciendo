from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.growth_record import GrowthRecord
from app.schemas.growth_record import GrowthCreate, GrowthUpdate
from app.services.base import BaseService
from app.repositories.growth_repository import GrowthRepository

class GrowthService(BaseService):
    def __init__(self, session: Session, growth_repo: GrowthRepository):
        super().__init__(session)
        self.growth_repo = growth_repo

    def _get_growth_record(self, baby_id: UUID, growth_id: UUID) -> GrowthRecord:
        record = self.growth_repo.get_by_id_and_baby_id(growth_id, baby_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de crecimiento no encontrado",
            )
        return record

    def create_growth_record(self, baby_id: UUID, payload: GrowthCreate) -> GrowthRecord:
        record = GrowthRecord(
            baby_id=baby_id,
            measured_at=payload.measured_at,
            weight_kg=payload.weight_kg,
            height_cm=payload.height_cm,
            head_circumference_cm=payload.head_circumference_cm,
            notes=payload.notes,
        )
        return self.growth_repo.add(record)

    def list_growth_records(self, baby_id: UUID) -> list[GrowthRecord]:
        return self.growth_repo.list_by_baby_id(baby_id)

    def get_growth_record_by_id(self, baby_id: UUID, growth_id: UUID) -> GrowthRecord:
        return self._get_growth_record(baby_id, growth_id)

    def update_growth_record(
        self,
        baby_id: UUID,
        growth_id: UUID,
        payload: GrowthUpdate,
    ) -> GrowthRecord:
        record = self._get_growth_record(baby_id, growth_id)
        update_data = payload.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se enviaron campos para actualizar",
            )

        for field, value in update_data.items():
            setattr(record, field, value)

        self.growth_repo.update()
        return record

    def delete_growth_record(self, baby_id: UUID, growth_id: UUID) -> None:
        record = self._get_growth_record(baby_id, growth_id)
        self.growth_repo.delete(record)
