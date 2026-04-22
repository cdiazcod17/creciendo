from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from .base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_email(self, email: str) -> User | None:
        return self.session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()
