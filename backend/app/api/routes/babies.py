from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.deps.auth import get_current_active_user
from app.api.deps.services import get_baby_service
from app.models.user import User
from app.schemas.baby import BabyCreate, BabyRead, BabyUpdate
from app.services.baby_service import BabyService

router = APIRouter()


@router.post("/", response_model=BabyRead, status_code=status.HTTP_201_CREATED)
def create_baby(
    payload: BabyCreate,
    current_user: User = Depends(get_current_active_user),
    service: BabyService = Depends(get_baby_service),
):
    return service.create_baby(payload, current_user)


@router.get("/", response_model=list[BabyRead], status_code=status.HTTP_200_OK)
def list_babies(
    current_user: User = Depends(get_current_active_user),
    service: BabyService = Depends(get_baby_service),
):
    return service.list_babies(current_user)


@router.get("/{baby_id}", response_model=BabyRead, status_code=status.HTTP_200_OK)
def get_baby(
    baby_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: BabyService = Depends(get_baby_service),
):
    return service.get_baby_by_id(baby_id, current_user)


@router.patch("/{baby_id}", response_model=BabyRead, status_code=status.HTTP_200_OK)
def update_baby(
    baby_id: UUID,
    payload: BabyUpdate,
    current_user: User = Depends(get_current_active_user),
    service: BabyService = Depends(get_baby_service),
):
    return service.update_baby(baby_id, payload, current_user)


@router.delete("/{baby_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_baby(
    baby_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: BabyService = Depends(get_baby_service),
):
    service.delete_baby(baby_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)