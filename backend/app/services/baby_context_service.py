from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.baby import Baby
from app.models.user import User


class BabyContextService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_owned_baby_or_404(self, user_id: UUID, baby_id: UUID | str) -> Baby:
        stmt = select(Baby).where(
            Baby.id == baby_id,
            Baby.user_id == user_id,
        )
        result = self.db.execute(stmt)
        baby = result.scalar_one_or_none()

        if baby is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bebé no encontrado.",
            )

        return baby

    def set_active_baby(self, user: User, baby_id: UUID | str) -> User:
        self.get_owned_baby_or_404(user_id=user.id, baby_id=baby_id)

        user.active_baby_id = baby_id
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user