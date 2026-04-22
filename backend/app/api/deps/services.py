from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.session import get_db
from app.services.auth_service import AuthService
from app.services.baby_service import BabyService
from app.services.event_service import EventService
from app.services.dashboard_service import DashboardService
from app.services.growth_service import GrowthService
from app.services.appointment_service import AppointmentService
from app.services.baby_context_service import BabyContextService
from app.services.health_notes import HealthNoteService

from app.repositories.user_repository import UserRepository
from app.repositories.baby_repository import BabyRepository
from app.repositories.event_repository import EventRepository
from app.repositories.growth_repository import GrowthRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.health_note_repository import HealthNoteRepository

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_baby_repository(db: Session = Depends(get_db)) -> BabyRepository:
    return BabyRepository(db)

def get_event_repository(db: Session = Depends(get_db)) -> EventRepository:
    return EventRepository(db)

def get_growth_repository(db: Session = Depends(get_db)) -> GrowthRepository:
    return GrowthRepository(db)

def get_appointment_repository(db: Session = Depends(get_db)) -> AppointmentRepository:
    return AppointmentRepository(db)

def get_health_note_repository(db: Session = Depends(get_db)) -> HealthNoteRepository:
    return HealthNoteRepository(db)

def get_auth_service(
    db: Session = Depends(get_db),
    user_repo: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(db, user_repo)

def get_baby_service(
    db: Session = Depends(get_db),
    baby_repo: BabyRepository = Depends(get_baby_repository)
) -> BabyService:
    return BabyService(db, baby_repo)

def get_event_service(
    db: Session = Depends(get_db),
    event_repo: EventRepository = Depends(get_event_repository)
) -> EventService:
    return EventService(db, event_repo)

def get_dashboard_service(
    db: Session = Depends(get_db),
    baby_repo: BabyRepository = Depends(get_baby_repository),
    event_repo: EventRepository = Depends(get_event_repository)
) -> DashboardService:
    return DashboardService(db, baby_repo, event_repo)

def get_growth_service(
    db: Session = Depends(get_db),
    growth_repo: GrowthRepository = Depends(get_growth_repository)
) -> GrowthService:
    return GrowthService(db, growth_repo)

def get_appointment_service(
    db: Session = Depends(get_db),
    appointment_repo: AppointmentRepository = Depends(get_appointment_repository)
) -> AppointmentService:
    return AppointmentService(db, appointment_repo)

def get_baby_context_service(
    db: Session = Depends(get_db),
    baby_repo: BabyRepository = Depends(get_baby_repository),
    user_repo: UserRepository = Depends(get_user_repository)
) -> BabyContextService:
    return BabyContextService(db, baby_repo, user_repo)

def get_health_note_service(
    db: Session = Depends(get_db),
    health_note_repo: HealthNoteRepository = Depends(get_health_note_repository)
) -> HealthNoteService:
    return HealthNoteService(db, health_note_repo)
