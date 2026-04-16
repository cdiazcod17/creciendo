from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.session import get_db
from app.services.auth_service import AuthService
from app.services.baby_service import BabyService
from app.services.baby_service import BabyService
from app.services.event_service import EventService
from app.services.dashboard_service import DashboardService
from app.services.growth_service import GrowthService
from app.services.appointment_service import AppointmentService

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

def get_baby_service(db: Session = Depends(get_db)) -> BabyService:
    return BabyService(db)

def get_baby_service(db: Session = Depends(get_db)) -> BabyService:
    return BabyService(db)

def get_event_service(db: Session = Depends(get_db)) -> EventService:
    return EventService(db)

def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(db)

def get_growth_service(db: Session = Depends(get_db)) -> GrowthService:
    return GrowthService(db)


def get_appointment_service(db: Session = Depends(get_db)) -> AppointmentService:
    return AppointmentService(db)
