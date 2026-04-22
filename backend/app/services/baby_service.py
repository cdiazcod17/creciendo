from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.baby import Baby
from app.models.user import User
from app.schemas.baby import BabyCreate, BabyUpdate
from app.services.base import BaseService
from app.repositories.baby_repository import BabyRepository

class BabyService(BaseService):
    def __init__(self, session: Session, baby_repo: BabyRepository):
        super().__init__(session)
        self.baby_repo = baby_repo

    def create_baby(self, payload: BabyCreate, current_user: User) -> Baby:
        baby = Baby(
            name=payload.name,
            birth_date=payload.birth_date,
            sex=payload.sex,
            notes=payload.notes,
            photo_url=payload.photo_url,
            user_id=current_user.id,
        )
        return self.baby_repo.add(baby)

    def list_babies(self, current_user: User) -> list[Baby]:
        return self.baby_repo.list_by_user_id(current_user.id)

    def get_baby_by_id(self, baby_id: UUID, current_user: User) -> Baby:
        baby = self.baby_repo.get_by_id_and_user_id(baby_id, current_user.id)
        if not baby:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bebé no encontrado",
            )
        return baby

    def update_baby(self, baby_id: UUID, payload: BabyUpdate, current_user: User) -> Baby:
        baby = self.get_baby_by_id(baby_id, current_user)
        update_data = payload.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se enviaron campos para actualizar",
            )

        for field, value in update_data.items():
            setattr(baby, field, value)

        self.baby_repo.update()
        return baby

    def delete_baby(self, baby_id: UUID, current_user: User) -> None:
        baby = self.get_baby_by_id(baby_id, current_user)
        self.baby_repo.delete(baby)
