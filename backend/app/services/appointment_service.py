from uuid import UUID

from fastapi import HTTPException, status

from app.models.appointment import Appointment
from app.models.baby import Baby
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.services.base import BaseService


class AppointmentService(BaseService):
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

    def _get_appointment(self, baby_id: UUID, appointment_id: UUID, current_user: User) -> Appointment:
        self._get_owned_baby(baby_id, current_user)

        appointment = (
            self.session.query(Appointment)
            .filter(
                Appointment.id == appointment_id,
                Appointment.baby_id == baby_id,
            )
            .first()
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada",
            )

        return appointment

    def create_appointment(self, baby_id: UUID, payload: AppointmentCreate, current_user: User) -> Appointment:
        self._get_owned_baby(baby_id, current_user)

        appointment = Appointment(
            baby_id=baby_id,
            title=payload.title,
            scheduled_at=payload.scheduled_at,
            status=payload.status,
            provider_name=payload.provider_name,
            location=payload.location,
            notes=payload.notes,
        )

        self.session.add(appointment)
        self.session.commit()
        self.session.refresh(appointment)
        return appointment

    def list_appointments(self, baby_id: UUID, current_user: User) -> list[Appointment]:
        self._get_owned_baby(baby_id, current_user)

        return (
            self.session.query(Appointment)
            .filter(Appointment.baby_id == baby_id)
            .order_by(Appointment.scheduled_at.desc())
            .all()
        )

    def get_appointment_by_id(self, baby_id: UUID, appointment_id: UUID, current_user: User) -> Appointment:
        return self._get_appointment(baby_id, appointment_id, current_user)

    def update_appointment(
        self,
        baby_id: UUID,
        appointment_id: UUID,
        payload: AppointmentUpdate,
        current_user: User,
    ) -> Appointment:
        appointment = self._get_appointment(baby_id, appointment_id, current_user)

        update_data = payload.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se enviaron campos para actualizar",
            )

        for field, value in update_data.items():
            setattr(appointment, field, value)

        self.session.commit()
        self.session.refresh(appointment)
        return appointment

    def delete_appointment(self, baby_id: UUID, appointment_id: UUID, current_user: User) -> None:
        appointment = self._get_appointment(baby_id, appointment_id, current_user)

        self.session.delete(appointment)
        self.session.commit()