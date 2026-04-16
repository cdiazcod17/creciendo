from fastapi import APIRouter
from app.api.routes import health,auth
from app.api.routes import babies
from app.api.routes import event
from app.api.routes import dashboard
from app.api.routes import growth_record
from app.api.routes import appointment

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router,prefix="/auth", tags=["auth"])
api_router.include_router(babies.router,prefix="/babies", tags=["babies"])
api_router.include_router(event.router,prefix="/babies/{baby_id}/events", tags=["event"])
api_router.include_router(dashboard.router,prefix="/dashboard", tags=["dashboard"])
api_router.include_router(appointment.router,prefix="/babies/{baby_id}/appointments", tags=["appointments"])