from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.deps.auth import get_current_active_user
from app.api.deps.services import get_appointment_service
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentRead, AppointmentUpdate
from app.services.appointment_service import AppointmentService

from app.api.deps.ownership import validate_baby_ownership
from app.models.baby import Baby

router = APIRouter()


@router.post("/", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    baby: Baby = Depends(validate_baby_ownership),
    service: AppointmentService = Depends(get_appointment_service),
):
    return service.create_appointment(baby.id, payload)


@router.get("/", response_model=list[AppointmentRead], status_code=status.HTTP_200_OK)
def list_appointments(
    baby: Baby = Depends(validate_baby_ownership),
    service: AppointmentService = Depends(get_appointment_service),
):
    return service.list_appointments(baby.id)


@router.get("/next", response_model=AppointmentRead | None, status_code=status.HTTP_200_OK)
def get_next_appointment(
    baby: Baby = Depends(validate_baby_ownership),
    service: AppointmentService = Depends(get_appointment_service),
):
    return service.get_next_appointment(baby.id)


@router.get("/{appointment_id}", response_model=AppointmentRead, status_code=status.HTTP_200_OK)
def get_appointment(
    appointment_id: UUID,
    baby: Baby = Depends(validate_baby_ownership),
    service: AppointmentService = Depends(get_appointment_service),
):
    return service.get_appointment_by_id(baby.id, appointment_id)


@router.patch("/{appointment_id}", response_model=AppointmentRead, status_code=status.HTTP_200_OK)
def update_appointment(
    appointment_id: UUID,
    payload: AppointmentUpdate,
    baby: Baby = Depends(validate_baby_ownership),
    service: AppointmentService = Depends(get_appointment_service),
):
    return service.update_appointment(baby.id, appointment_id, payload)


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(
    appointment_id: UUID,
    baby: Baby = Depends(validate_baby_ownership),
    service: AppointmentService = Depends(get_appointment_service),
):
    service.delete_appointment(baby.id, appointment_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)