from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status

from app.api.deps.auth import get_current_active_user
from app.api.deps.services import get_health_note_service
from app.api.deps.ownership import get_target_baby
from app.models.user import User
from app.models.baby import Baby
from app.schemas.health_note import HealthNoteCreate, HealthNoteRead, HealthNoteUpdate
from app.services.health_notes import HealthNoteService

router = APIRouter()


@router.get("/", response_model=list[HealthNoteRead])
def list_health_notes(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    note_type: str | None = Query(default=None, min_length=1, max_length=60),
    title_contains: str | None = Query(default=None, min_length=1, max_length=120),
    recorded_from: datetime | None = Query(default=None),
    recorded_to: datetime | None = Query(default=None),
    baby: Baby = Depends(get_target_baby),
    service: HealthNoteService = Depends(get_health_note_service),
):
    return service.list_health_notes(
        baby_id=baby.id,
        limit=limit,
        offset=offset,
        note_type=note_type,
        title_contains=title_contains,
        recorded_from=recorded_from,
        recorded_to=recorded_to,
    )


@router.post("/", response_model=HealthNoteRead, status_code=status.HTTP_201_CREATED)
def create_health_note(
    payload: HealthNoteCreate = ...,
    baby: Baby = Depends(get_target_baby),
    service: HealthNoteService = Depends(get_health_note_service),
):
    payload.baby_id = baby.id
    return service.create_health_note(
        payload=payload,
    )


@router.get("/{health_note_id}", response_model=HealthNoteRead)
def get_health_note(
    health_note_id: UUID = Path(...),
    baby: Baby = Depends(get_target_baby),
    service: HealthNoteService = Depends(get_health_note_service),
):
    return service.get_health_note(
        baby_id=baby.id,
        health_note_id=health_note_id,
    )


@router.patch("/{health_note_id}", response_model=HealthNoteRead)
def update_health_note(
    health_note_id: UUID = Path(...),
    payload: HealthNoteUpdate = ...,
    baby: Baby = Depends(get_target_baby),
    service: HealthNoteService = Depends(get_health_note_service),
):
    return service.update_health_note(
        baby_id=baby.id,
        health_note_id=health_note_id,
        payload=payload,
    )


@router.delete("/{health_note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_health_note(
    health_note_id: UUID = Path(...),
    baby: Baby = Depends(get_target_baby),
    service: HealthNoteService = Depends(get_health_note_service),
):
    service.delete_health_note(
        baby_id=baby.id,
        health_note_id=health_note_id,
    )
