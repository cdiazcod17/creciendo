# app/api/routes/growth.py
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.deps.auth import get_current_active_user
from app.api.deps.services import get_growth_service
from app.models.user import User
from app.schemas.growth_record import GrowthCreate, GrowthRead, GrowthUpdate
from app.services.growth_service import GrowthService

router = APIRouter()

@router.post("/", response_model=GrowthRead, status_code=status.HTTP_201_CREATED)
def create_growth_record(
    baby_id: UUID,
    payload: GrowthCreate,
    current_user: User = Depends(get_current_active_user),
    service: GrowthService = Depends(get_growth_service),
):
    return service.create_growth_record(baby_id, payload, current_user)


@router.get("/", response_model=list[GrowthRead], status_code=status.HTTP_200_OK)
def list_growth_records(
    baby_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: GrowthService = Depends(get_growth_service),
):
    return service.list_growth_records(baby_id, current_user)


@router.get("/{growth_id}", response_model=GrowthRead, status_code=status.HTTP_200_OK)
def get_growth_record(
    baby_id: UUID,
    growth_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: GrowthService = Depends(get_growth_service),
):
    return service.get_growth_record_by_id(baby_id, growth_id, current_user)


@router.patch("/{growth_id}", response_model=GrowthRead, status_code=status.HTTP_200_OK)
def update_growth_record(
    baby_id: UUID,
    growth_id: UUID,
    payload: GrowthUpdate,
    current_user: User = Depends(get_current_active_user),
    service: GrowthService = Depends(get_growth_service),
):
    return service.update_growth_record(baby_id, growth_id, payload, current_user)


@router.delete("/{growth_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_growth_record(
    baby_id: UUID,
    growth_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: GrowthService = Depends(get_growth_service),
):
    service.delete_growth_record(baby_id, growth_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)