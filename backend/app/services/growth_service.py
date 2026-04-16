# app/services/growth_service.py
from uuid import UUID

from fastapi import HTTPException, status

from app.models.baby import Baby
from app.models.growth_record import GrowthRecord
from app.models.user import User
from app.schemas.growth_record import GrowthCreate, GrowthUpdate
from app.services.base import BaseService


class GrowthService(BaseService):
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

    def _get_growth_record(self, baby_id: UUID, growth_id: UUID, current_user: User) -> GrowthRecord:
        self._get_owned_baby(baby_id, current_user)

        record = (
            self.session.query(GrowthRecord)
            .filter(
                GrowthRecord.id == growth_id,
                GrowthRecord.baby_id == baby_id,
            )
            .first()
        )

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de crecimiento no encontrado",
            )

        return record

    def create_growth_record(self, baby_id: UUID, payload: GrowthCreate, current_user: User) -> GrowthRecord:
        self._get_owned_baby(baby_id, current_user)

        record = GrowthRecord(
            baby_id=baby_id,
            measured_at=payload.measured_at,
            weight_kg=payload.weight_kg,
            height_cm=payload.height_cm,
            head_circumference_cm=payload.head_circumference_cm,
            notes=payload.notes,
        )

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def list_growth_records(self, baby_id: UUID, current_user: User) -> list[GrowthRecord]:
        self._get_owned_baby(baby_id, current_user)

        return (
            self.session.query(GrowthRecord)
            .filter(GrowthRecord.baby_id == baby_id)
            .order_by(GrowthRecord.measured_at.desc())
            .all()
        )

    def get_growth_record_by_id(self, baby_id: UUID, growth_id: UUID, current_user: User) -> GrowthRecord:
        return self._get_growth_record(baby_id, growth_id, current_user)

    def update_growth_record(
        self,
        baby_id: UUID,
        growth_id: UUID,
        payload: GrowthUpdate,
        current_user: User,
    ) -> GrowthRecord:
        record = self._get_growth_record(baby_id, growth_id, current_user)

        update_data = payload.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se enviaron campos para actualizar",
            )

        for field, value in update_data.items():
            setattr(record, field, value)

        self.session.commit()
        self.session.refresh(record)
        return record

    def delete_growth_record(self, baby_id: UUID, growth_id: UUID, current_user: User) -> None:
        record = self._get_growth_record(baby_id, growth_id, current_user)

        self.session.delete(record)
        self.session.commit()