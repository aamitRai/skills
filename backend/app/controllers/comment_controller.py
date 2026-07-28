"""Comment controller — HTTP-level handling for comment endpoints."""

import logging

from fastapi import status
from fastapi.responses import Response

from app.schemas.comment_schemas import (
    CommentCreateRequest,
    CommentResponse,
)
from app.services.comment_service import CommentService

logger = logging.getLogger(__name__)


class CommentController:
    """Controller for comment endpoints."""

    def __init__(self, service: CommentService) -> None:
        self._service = service

    async def list_by_skill_id(self, skill_id: str) -> list[CommentResponse]:
        """GET /skills/{skill_id}/comments — Get all comments for a skill."""
        return await self._service.get_by_skill_id(skill_id)

    async def create(
        self, skill_id: str, payload: CommentCreateRequest
    ) -> CommentResponse:
        """POST /skills/{skill_id}/comments — Create a comment on a skill."""
        return await self._service.create(skill_id, payload)

    async def delete(self, comment_id: str) -> Response:
        """DELETE /skills/{skill_id}/comments/{comment_id} — Delete a comment."""
        await self._service.delete(comment_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
