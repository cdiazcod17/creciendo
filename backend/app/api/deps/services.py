from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.session import get_db
from app.services.auth_service import AuthService
from app.services.baby_service import BabyService


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

def get_baby_service(db: Session = Depends(get_db)) -> BabyService:
    return BabyService(db)