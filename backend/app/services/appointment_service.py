from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.services.base import BaseService
from app.repositories.appointment_repository import AppointmentRepository

class AppointmentService(BaseService):
    def __init__(self, session: Session, appointment_repo: AppointmentRepository):
        super().__init__(session)
        self.appointment_repo = appointment_repo

    def _get_appointment(self, baby_id: UUID, appointment_id: UUID) -> Appointment:
        appointment = self.appointment_repo.get_by_id_and_baby_id(appointment_id, baby_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada",
            )
        return appointment

    def create_appointment(self, baby_id: UUID, payload: AppointmentCreate) -> Appointment:
        appointment = Appointment(
            baby_id=baby_id,
            title=payload.title,
            scheduled_at=payload.scheduled_at,
            status=payload.status,
            provider_name=payload.provider_name,
            location=payload.location,
            notes=payload.notes,
        )
        return self.appointment_repo.add(appointment)

    def list_appointments(self, baby_id: UUID) -> list[Appointment]:
        return self.appointment_repo.list_by_baby_id(baby_id)

    def get_next_appointment(self, baby_id: UUID) -> Appointment | None:
        return self.appointment_repo.get_next_by_baby_id(baby_id)

    def get_appointment_by_id(self, baby_id: UUID, appointment_id: UUID) -> Appointment:
        return self._get_appointment(baby_id, appointment_id)

    def update_appointment(
        self,
        baby_id: UUID,
        appointment_id: UUID,
        payload: AppointmentUpdate,
    ) -> Appointment:
        appointment = self._get_appointment(baby_id, appointment_id)
        update_data = payload.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se enviaron campos para actualizar",
            )

        for field, value in update_data.items():
            setattr(appointment, field, value)

        self.appointment_repo.update()
        return appointment

    def delete_appointment(self, baby_id: UUID, appointment_id: UUID) -> None:
        appointment = self._get_appointment(baby_id, appointment_id)
        self.appointment_repo.delete(appointment)
