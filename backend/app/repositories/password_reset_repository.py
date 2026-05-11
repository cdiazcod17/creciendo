from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.password_reset import PasswordResetToken
from .base import BaseRepository

class PasswordResetRepository(BaseRepository[PasswordResetToken]):
    def __init__(self, session: Session):
        super().__init__(PasswordResetToken, session)

    def get_by_token(self, token: str) -> PasswordResetToken | None:
        return self.session.execute(
            select(PasswordResetToken).where(PasswordResetToken.token == token)
        ).scalar_one_or_none()

    def delete_by_user_id(self, user_id: str) -> None:
        tokens = self.session.execute(
            select(PasswordResetToken).where(PasswordResetToken.user_id == user_id)
        ).scalars().all()
        for token in tokens:
            self.session.delete(token)
        self.session.commit()
