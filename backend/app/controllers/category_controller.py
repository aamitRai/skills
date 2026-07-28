"""Category controller — HTTP-level handling for category endpoints."""

import logging

from fastapi import HTTPException, status
from fastapi.responses import Response

from app.constants import error_messages as err
from app.constants import log_messages as log
from app.schemas.category_schemas import (
    CategoryCreateRequest,
    CategoryResponse,
    CategoryUpdateRequest,
)
from app.services.category_service import CategoryService

logger = logging.getLogger(__name__)


class CategoryController:
    """Controller for category endpoints."""

    def __init__(self, service: CategoryService) -> None:
        self._service = service

    async def list_all(self, user_id: str) -> list[CategoryResponse]:
        """GET /categories — Get all categories for the current user."""
        return await self._service.get_all(user_id)

    async def create(
        self, user_id: str, payload: CategoryCreateRequest
    ) -> CategoryResponse:
        """POST /categories — Create a new category."""
        return await self._service.create(user_id, payload)

    async def get_by_id(self, category_id: str) -> CategoryResponse:
        """GET /categories/{category_id} — Get a single category."""
        return await self._service.get_by_id(category_id)

    async def update(
        self, category_id: str, payload: CategoryUpdateRequest
    ) -> CategoryResponse:
        """PATCH /categories/{category_id} — Update a category."""
        return await self._service.update(category_id, payload)

    async def delete(self, category_id: str) -> Response:
        """DELETE /categories/{category_id} — Delete a category."""
        await self._service.delete(category_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
