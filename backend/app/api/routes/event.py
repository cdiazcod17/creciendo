from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.deps.auth import get_current_active_user
from app.api.deps.services import get_event_service
from app.models.user import User
from app.schemas.event import EventCreate, EventRead,EventUpdate
from app.services.event_service import EventService

router = APIRouter()


@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(
    baby_id: UUID,
    payload: EventCreate,
    current_user: User = Depends(get_current_active_user),
    service: EventService = Depends(get_event_service),
):
    return service.create_event(baby_id, payload, current_user)


@router.get("/", response_model=list[EventRead], status_code=status.HTTP_200_OK)
def list_events(
    baby_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: EventService = Depends(get_event_service),
):
    return service.list_events(baby_id, current_user)


@router.get("/{event_id}", response_model=EventRead, status_code=status.HTTP_200_OK)
def get_event(
    baby_id: UUID,
    event_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: EventService = Depends(get_event_service),
):
    return service.get_event_by_id(baby_id, event_id, current_user)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    baby_id: UUID,
    event_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: EventService = Depends(get_event_service),
):
    service.delete_event(baby_id, event_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{event_id}", response_model=EventRead, status_code=status.HTTP_200_OK)
def update_event(
    baby_id: UUID,
    event_id: UUID,
    payload: EventUpdate,
    current_user: User = Depends(get_current_active_user),
    service: EventService = Depends(get_event_service),
):
    return service.update_event(baby_id, event_id, payload, current_user)