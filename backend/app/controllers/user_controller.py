"""User controller — HTTP-level handling for user profile endpoints."""

import logging

from fastapi import HTTPException, status

from app.constants import error_messages as err
from app.constants import log_messages as log
from app.schemas.user_schemas import (
    SettingsResponse,
    SettingsUpdateRequest,
    UserResponse,
    UserUpdateRequest,
)
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)


class UserController:
    """Controller for user profile and settings endpoints."""

    def __init__(self, service: AuthService) -> None:
        self._service = service

    async def get_profile(self, user_id: str) -> UserResponse:
        """GET /users/me — Get the current user's profile."""
        return await self._service.get_current_user(user_id)

    async def update_profile(
        self, user_id: str, payload: UserUpdateRequest
    ) -> UserResponse:
        """PATCH /users/me — Update the current user's profile."""
        return await self._service.update_profile(user_id, payload)

    async def get_settings(self, user_id: str) -> SettingsResponse:
        """GET /users/me/settings — Get the current user's settings."""
        return await self._service.get_settings(user_id)

    async def update_settings(
        self, user_id: str, payload: SettingsUpdateRequest
    ) -> SettingsResponse:
        """PATCH /users/me/settings — Update the current user's settings."""
        return await self._service.update_settings(user_id, payload)
