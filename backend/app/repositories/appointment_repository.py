from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.appointment import Appointment
from app.core.enums import AppointmentStatus
from .base import BaseRepository

class AppointmentRepository(BaseRepository[Appointment]):
    def __init__(self, session: Session):
        super().__init__(Appointment, session)

    def list_by_baby_id(self, baby_id: UUID) -> list[Appointment]:
        return list(
            self.session.execute(
                select(Appointment)
                .where(Appointment.baby_id == baby_id)
                .order_by(Appointment.scheduled_at.desc())
            ).scalars().all()
        )

    def get_by_id_and_baby_id(self, appointment_id: UUID, baby_id: UUID) -> Appointment | None:
        return self.session.execute(
            select(Appointment).where(
                Appointment.id == appointment_id,
                Appointment.baby_id == baby_id
            )
        ).scalar_one_or_none()

    def get_next_by_baby_id(self, baby_id: UUID) -> Appointment | None:
        return self.session.execute(
            select(Appointment)
            .where(
                Appointment.baby_id == baby_id,
                Appointment.scheduled_at >= datetime.now(timezone.utc),
                Appointment.status == AppointmentStatus.scheduled,
            )
            .order_by(Appointment.scheduled_at.asc())
            .limit(1)
        ).scalar_one_or_none()
