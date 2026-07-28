"""Progress controller — HTTP-level handling for progress endpoints."""

import logging

from app.schemas.progress_schemas import ProgressResponse, ProgressUpdateRequest
from app.services.progress_service import ProgressService

logger = logging.getLogger(__name__)


class ProgressController:
    """Controller for progress endpoints."""

    def __init__(self, service: ProgressService) -> None:
        self._service = service

    async def list_all(self) -> list[ProgressResponse]:
        """GET /progress — Get all progress records."""
        return await self._service.get_all()

    async def get_by_skill_id(self, skill_id: str) -> ProgressResponse:
        """GET /skills/{skill_id}/progress — Get progress for a skill."""
        return await self._service.get_by_skill_id(skill_id)

    async def update(
        self, skill_id: str, payload: ProgressUpdateRequest
    ) -> ProgressResponse:
        """PUT /skills/{skill_id}/progress — Update progress for a skill."""
        return await self._service.update(skill_id, payload)
