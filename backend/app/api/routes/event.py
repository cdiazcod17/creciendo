from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.deps.auth import get_current_active_user
from app.api.deps.services import get_event_service
from app.models.user import User
from app.schemas.event import EventCreate, EventRead,EventUpdate
from app.services.event_service import EventService

from app.api.deps.ownership import validate_baby_ownership
from app.models.baby import Baby

router = APIRouter()


@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(
    payload: EventCreate,
    baby: Baby = Depends(validate_baby_ownership),
    service: EventService = Depends(get_event_service),
):
    return service.create_event(baby.id, payload)


@router.get("/", response_model=list[EventRead], status_code=status.HTTP_200_OK)
def list_events(
    baby: Baby = Depends(validate_baby_ownership),
    service: EventService = Depends(get_event_service),
):
    return service.list_events(baby.id)


@router.get("/{event_id}", response_model=EventRead, status_code=status.HTTP_200_OK)
def get_event(
    event_id: UUID,
    baby: Baby = Depends(validate_baby_ownership),
    service: EventService = Depends(get_event_service),
):
    return service.get_event_by_id(baby.id, event_id)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: UUID,
    baby: Baby = Depends(validate_baby_ownership),
    service: EventService = Depends(get_event_service),
):
    service.delete_event(baby.id, event_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{event_id}", response_model=EventRead, status_code=status.HTTP_200_OK)
def update_event(
    event_id: UUID,
    payload: EventUpdate,
    baby: Baby = Depends(validate_baby_ownership),
    service: EventService = Depends(get_event_service),
):
    return service.update_event(baby.id, event_id, payload)