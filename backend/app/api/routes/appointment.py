from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.deps.auth import get_current_active_user
from app.api.deps.services import get_appointment_service
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentRead, AppointmentUpdate
from app.services.appointment_service import AppointmentService

router = APIRouter()


@router.post("/", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(
    baby_id: UUID,
    payload: AppointmentCreate,
    current_user: User = Depends(get_current_active_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    return service.create_appointment(baby_id, payload, current_user)


@router.get("/", response_model=list[AppointmentRead], status_code=status.HTTP_200_OK)
def list_appointments(
    baby_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    return service.list_appointments(baby_id, current_user)


@router.get("/{appointment_id}", response_model=AppointmentRead, status_code=status.HTTP_200_OK)
def get_appointment(
    baby_id: UUID,
    appointment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    return service.get_appointment_by_id(baby_id, appointment_id, current_user)


@router.patch("/{appointment_id}", response_model=AppointmentRead, status_code=status.HTTP_200_OK)
def update_appointment(
    baby_id: UUID,
    appointment_id: UUID,
    payload: AppointmentUpdate,
    current_user: User = Depends(get_current_active_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    return service.update_appointment(baby_id, appointment_id, payload, current_user)


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(
    baby_id: UUID,
    appointment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    service.delete_appointment(baby_id, appointment_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)