# app/api/routes/growth.py
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.deps.auth import get_current_active_user
from app.api.deps.services import get_growth_service
from app.models.user import User
from app.schemas.growth_record import GrowthCreate, GrowthRead, GrowthUpdate
from app.services.growth_service import GrowthService

from app.api.deps.ownership import validate_baby_ownership
from app.models.baby import Baby

router = APIRouter()

@router.post("/", response_model=GrowthRead, status_code=status.HTTP_201_CREATED)
def create_growth_record(
    payload: GrowthCreate,
    baby: Baby = Depends(validate_baby_ownership),
    service: GrowthService = Depends(get_growth_service),
):
    return service.create_growth_record(baby.id, payload)


@router.get("/", response_model=list[GrowthRead], status_code=status.HTTP_200_OK)
def list_growth_records(
    baby: Baby = Depends(validate_baby_ownership),
    service: GrowthService = Depends(get_growth_service),
):
    return service.list_growth_records(baby.id)


@router.get("/{growth_id}", response_model=GrowthRead, status_code=status.HTTP_200_OK)
def get_growth_record(
    growth_id: UUID,
    baby: Baby = Depends(validate_baby_ownership),
    service: GrowthService = Depends(get_growth_service),
):
    return service.get_growth_record_by_id(baby.id, growth_id)


@router.patch("/{growth_id}", response_model=GrowthRead, status_code=status.HTTP_200_OK)
def update_growth_record(
    growth_id: UUID,
    payload: GrowthUpdate,
    baby: Baby = Depends(validate_baby_ownership),
    service: GrowthService = Depends(get_growth_service),
):
    return service.update_growth_record(baby.id, growth_id, payload)


@router.delete("/{growth_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_growth_record(
    growth_id: UUID,
    baby: Baby = Depends(validate_baby_ownership),
    service: GrowthService = Depends(get_growth_service),
):
    service.delete_growth_record(baby.id, growth_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)