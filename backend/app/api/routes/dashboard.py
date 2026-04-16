from fastapi import APIRouter, Depends, status

from app.api.deps.auth import get_current_active_user
from app.api.deps.services import get_dashboard_service
from app.models.user import User
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/me", response_model=DashboardSummary, status_code=status.HTTP_200_OK)
def get_my_dashboard(
    current_user: User = Depends(get_current_active_user),
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.get_user_dashboard(current_user)