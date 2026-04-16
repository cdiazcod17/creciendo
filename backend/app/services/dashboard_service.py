from app.models.baby import Baby
from app.models.event import Event
from app.models.user import User
from app.services.base import BaseService


class DashboardService(BaseService):
    def get_user_dashboard(self, current_user: User) -> dict:
        babies = (
            self.session.query(Baby)
            .filter(Baby.user_id == current_user.id)
            .order_by(Baby.created_at.desc())
            .all()
        )

        baby_ids = [baby.id for baby in babies]

        total_events = 0
        recent_events = []

        if baby_ids:
            total_events = (
                self.session.query(Event)
                .filter(Event.baby_id.in_(baby_ids))
                .count()
            )

            events = (
                self.session.query(Event, Baby.full_name.label("baby_name"))
                .join(Baby, Event.baby_id == Baby.id)
                .filter(Baby.user_id == current_user.id)
                .order_by(Event.occurred_at.desc())
                .limit(5)
                .all()
            )

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
                for event, baby_name in events
            ]

        babies_summary = []

        for baby in babies:
            last_event = (
                self.session.query(Event)
                .filter(Event.baby_id == baby.id)
                .order_by(Event.occurred_at.desc())
                .first()
            )

            babies_summary.append(
                {
                    "id": baby.id,
                    "full_name": baby.full_name,
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