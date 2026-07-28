"""Skill controller — HTTP-level handling for skill endpoints."""

import logging

from fastapi import status
from fastapi.responses import Response

from app.schemas.category_schemas import (
    SkillCreateRequest,
    SkillMoveRequest,
    SkillResponse,
    SkillUpdateRequest,
)
from app.services.category_service import CategoryService

logger = logging.getLogger(__name__)


class SkillController:
    """Controller for skill endpoints."""

    def __init__(self, service: CategoryService) -> None:
        self._service = service

    async def create(
        self, category_id: str, payload: SkillCreateRequest
    ) -> SkillResponse:
        """POST /categories/{category_id}/skills — Add a skill to a category."""
        return await self._service.add_skill(category_id, payload)

    async def get_by_id(self, skill_id: str) -> SkillResponse:
        """GET /skills/{skill_id} — Get a single skill."""
        return await self._service.get_skill(skill_id)

    async def update(
        self, skill_id: str, payload: SkillUpdateRequest
    ) -> SkillResponse:
        """PATCH /skills/{skill_id} — Update a skill."""
        return await self._service.update_skill(skill_id, payload)

    async def delete(self, skill_id: str) -> Response:
        """DELETE /skills/{skill_id} — Delete a skill."""
        await self._service.delete_skill(skill_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def move(
        self, skill_id: str, payload: SkillMoveRequest
    ) -> dict:
        """PATCH /skills/{skill_id}/move — Move a skill up or down."""
        return await self._service.move_skill(skill_id, payload)
