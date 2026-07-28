"""
Dashboard route handlers.

HTTP endpoints for dashboard summary data and activity feed.
"""

from fastapi import APIRouter, Depends, status

from app.controllers.dashboard_controller import DashboardController
from app.dependencies import get_dashboard_controller
from app.middleware.auth_middleware import get_current_user_id
from app.schemas.dashboard_schemas import ActivityItem, DashboardSummaryResponse

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_summary(
    user_id: str = Depends(get_current_user_id),
    controller: DashboardController = Depends(get_dashboard_controller),
) -> DashboardSummaryResponse:
    """Get the dashboard summary for the current user."""
    return await controller.get_summary(user_id)


@router.get(
    "/activity",
    response_model=list[ActivityItem],
    status_code=status.HTTP_200_OK,
)
async def get_activity(
    user_id: str = Depends(get_current_user_id),
    controller: DashboardController = Depends(get_dashboard_controller),
) -> list[ActivityItem]:
    """Get the recent activity feed for the current user."""
    return await controller.get_activity(user_id)
