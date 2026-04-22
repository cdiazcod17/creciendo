from uuid import UUID
from fastapi import Depends, HTTPException, status, Path
from app.models.user import User
from app.models.baby import Baby
from app.api.deps.auth import get_current_active_user
from app.api.deps.services import get_baby_repository
from app.repositories.baby_repository import BabyRepository

def validate_baby_ownership(
    baby_id: UUID = Path(...),
    current_user: User = Depends(get_current_active_user),
    baby_repo: BabyRepository = Depends(get_baby_repository)
) -> Baby:
    baby = baby_repo.get_by_id_and_user_id(baby_id, current_user.id)
    if not baby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bebé no encontrado o no tienes permisos para acceder a él."
        )
    return baby

def get_target_baby(
    baby_id: UUID | None = None,
    current_user: User = Depends(get_current_active_user),
    baby_repo: BabyRepository = Depends(get_baby_repository)
) -> Baby:
    target_id = baby_id or current_user.active_baby_id
    if not target_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionó baby_id y no hay un bebé activo seleccionado."
        )
    
    # Ensure target_id is UUID object if it came from current_user.active_baby_id (which is str | None in model)
    if isinstance(target_id, str):
        try:
            target_id = UUID(target_id)
        except ValueError:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de bebé inválido."
            )

    baby = baby_repo.get_by_id_and_user_id(target_id, current_user.id)
    if not baby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bebé no encontrado o no tienes permisos."
        )
    return baby
