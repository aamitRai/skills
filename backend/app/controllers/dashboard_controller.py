"""Dashboard controller — HTTP-level handling for dashboard endpoints."""

import logging

from app.schemas.dashboard_schemas import ActivityItem, DashboardSummaryResponse
from app.services.dashboard_service import DashboardService

logger = logging.getLogger(__name__)


class DashboardController:
    """Controller for dashboard endpoints."""

    def __init__(self, service: DashboardService) -> None:
        self._service = service

    async def get_summary(self, user_id: str) -> DashboardSummaryResponse:
        """GET /dashboard/summary — Get dashboard summary."""
        return await self._service.get_summary(user_id)

    async def get_activity(self, user_id: str) -> list[ActivityItem]:
        """GET /dashboard/activity — Get recent activity feed."""
        return await self._service.get_activity(user_id)
