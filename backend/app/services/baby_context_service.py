from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.baby import Baby
from app.models.user import User
from app.repositories.baby_repository import BabyRepository
from app.repositories.user_repository import UserRepository

class BabyContextService:
    def __init__(self, session: Session, baby_repo: BabyRepository, user_repo: UserRepository) -> None:
        self.session = session
        self.baby_repo = baby_repo
        self.user_repo = user_repo

    def get_owned_baby_or_404(self, user_id: UUID, baby_id: UUID | str) -> Baby:
        baby = self.baby_repo.get_by_id_and_user_id(UUID(str(baby_id)), user_id)

        if baby is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bebé no encontrado.",
            )

        return baby

    def set_active_baby(self, user: User, baby_id: UUID | str) -> User:
        target_uuid = UUID(str(baby_id))
        self.get_owned_baby_or_404(user_id=user.id, baby_id=target_uuid)

        user.active_baby_id = target_uuid
        self.user_repo.update()
        return user
