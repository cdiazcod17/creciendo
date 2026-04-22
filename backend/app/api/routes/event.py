from uuid import UUID

from fastapi import APIRouter, Depends, Response, status, Query

from app.api.deps.services import get_event_service
from app.api.deps.ownership import validate_baby_ownership
from app.models.baby import Baby
from app.schemas.event import EventCreate, EventRead, EventUpdate
from app.services.event_service import EventService
from app.core.enums import EventType

router = APIRouter()


@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(
    payload: EventCreate,
    baby: Baby = Depends(validate_baby_ownership),
    service: EventService = Depends(get_event_service),
):
    """Crea un nuevo evento para el bebé especificado."""
    return service.create_event(baby.id, payload)


@router.get("/", response_model=list[EventRead], status_code=status.HTTP_200_OK)
def list_events(
    event_type: EventType | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    baby: Baby = Depends(validate_baby_ownership),
    service: EventService = Depends(get_event_service),
):
    """Lista los eventos de un bebé con filtros y paginación."""
    return service.list_events(baby.id, event_type, limit, offset)


@router.get("/{event_id}", response_model=EventRead, status_code=status.HTTP_200_OK)
def get_event(
    event_id: UUID,
    baby: Baby = Depends(validate_baby_ownership),
    service: EventService = Depends(get_event_service),
):
    """Obtiene el detalle de un evento específico."""
    return service.get_event_by_id(baby.id, event_id)


@router.patch("/{event_id}", response_model=EventRead, status_code=status.HTTP_200_OK)
def update_event(
    event_id: UUID,
    payload: EventUpdate,
    baby: Baby = Depends(validate_baby_ownership),
    service: EventService = Depends(get_event_service),
):
    """Actualiza un evento existente."""
    return service.update_event(baby.id, event_id, payload)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: UUID,
    baby: Baby = Depends(validate_baby_ownership),
    service: EventService = Depends(get_event_service),
):
    """Elimina un evento."""
    service.delete_event(baby.id, event_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
