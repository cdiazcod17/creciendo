# app/services/baby_service.py
from uuid import UUID

from fastapi import HTTPException, status

from app.models.baby import Baby
from app.models.user import User
from app.schemas.baby import BabyCreate, BabyUpdate
from app.services.base import BaseService


class BabyService(BaseService):
    def create_baby(self, payload: BabyCreate, current_user: User) -> Baby:
        baby = Baby(
            full_name=payload.full_name,
            birth_date=payload.birth_date,
            sex=payload.sex,
            user_id=current_user.id,
        )

        self.session.add(baby)
        self.session.commit()
        self.session.refresh(baby)
        return baby

    def list_babies(self, current_user: User) -> list[Baby]:
        return (
            self.session.query(Baby)
            .filter(Baby.user_id == current_user.id)
            .order_by(Baby.created_at.desc())
            .all()
        )

    def get_baby_by_id(self, baby_id: UUID, current_user: User) -> Baby:
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

        self.session.commit()
        self.session.refresh(baby)
        return baby

    def delete_baby(self, baby_id: UUID, current_user: User) -> None:
        baby = self.get_baby_by_id(baby_id, current_user)

        self.session.delete(baby)
        self.session.commit()