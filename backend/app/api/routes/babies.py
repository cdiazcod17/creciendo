from fastapi import APIRouter, HTTPException, status, Depends,Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.api.deps.auth import get_current_user,get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.models.baby import Baby
from app.schemas.baby import BabyCreate, BabyRead,BabyUpdate


router = APIRouter()

@router.post("/", response_model=BabyRead, status_code=status.HTTP_201_CREATED)
def create_baby(
    baby_in: BabyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    baby = Baby(**baby_in.model_dump(), user_id=current_user.id)
    db.add(baby)
    db.commit()
    db.refresh(baby)
    return baby


@router.get("/", response_model=List[BabyRead])
def get_babies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    babies = db.query(Baby).filter(Baby.user_id == current_user.id).all()
    return babies


@router.get("/{baby_id}", response_model=BabyRead)
def get_baby(
    baby_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    baby = db.query(Baby).filter(
        Baby.id == baby_id,
        Baby.user_id == current_user.id
    ).first()
    
    if not baby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bebé no encontrado"
        )
    return baby

@router.patch("/{baby_id}", response_model=BabyRead)
def update_baby(
    baby_id: UUID,
    payload: BabyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    baby = db.query(Baby).filter(
        Baby.id == baby_id,
        Baby.user_id == current_user.id
    ).first()

    if not baby:
        raise HTTPException(status_code=404, detail="Bebé no encontrado")

    update_data = payload.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se enviaron campos para actualizar"
        )
        
    for key, value in update_data.items():
        setattr(baby, key, value)

    db.commit()
    db.refresh(baby)
    return baby

@router.delete("/{baby_id}")
def delete_baby(
    baby_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    baby = db.query(Baby).filter(
        Baby.id == baby_id,
        Baby.user_id == current_user.id
    ).first()
    
    if not baby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bebé no encontrado"
        )
    
    db.delete(baby)
    db.commit()
    return {"detail": "Bebé eliminado exitosamente"}