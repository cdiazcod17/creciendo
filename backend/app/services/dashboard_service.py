from sqlalchemy.orm import Session
from app.models.user import User
from app.services.base import BaseService
from app.repositories.baby_repository import BabyRepository
from app.repositories.event_repository import EventRepository

class DashboardService(BaseService):
    def __init__(self, session: Session, baby_repo: BabyRepository, event_repo: EventRepository):
        super().__init__(session)
        self.baby_repo = baby_repo
        self.event_repo = event_repo

    def get_user_dashboard(self, current_user: User) -> dict:
        babies = self.baby_repo.list_by_user_id(current_user.id)
        baby_ids = [baby.id for baby in babies]

        total_events = self.event_repo.count_by_baby_ids(baby_ids)
        recent_events_raw = self.event_repo.list_recent_with_baby_name_by_user_id(current_user.id)

        recent_events = [
            {
                "id": event.id,
                "baby_id": event.baby_id,
                "baby_name": baby_name,
                "event_type": event.event_type,
                "occurred_at": event.occurred_at,
                "amount": event.amount,
                "notes": event.notes,
            }
            for event, baby_name in recent_events_raw
        ]

        babies_summary = []
        for baby in babies:
            last_event = self.event_repo.get_latest_by_baby_id(baby.id)
            babies_summary.append(
                {
                    "id": baby.id,
                    "name": baby.name,
                    "last_event": (
                        {
                            "id": last_event.id,
                            "event_type": last_event.event_type,
                            "occurred_at": last_event.occurred_at,
                            "amount": last_event.amount,
                            "notes": last_event.notes,
                        }
                        if last_event
                        else None
                    ),
                }
            )

        return {
            "user_id": current_user.id,
            "full_name": current_user.full_name,
            "total_babies": len(babies),
            "total_events": total_events,
            "babies": babies_summary,
            "recent_events": recent_events,
        }
