"""Auth controller — HTTP-level handling for auth endpoints."""

import logging

from fastapi import HTTPException, status

from app.constants import error_messages as err
from app.constants import log_messages as log
from app.constants.http_status import HTTP_401_UNAUTHORIZED
from app.exceptions.app_exceptions import InvalidCredentialsError
from app.schemas.user_schemas import LoginRequest, LoginResponse, UserResponse
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)


class AuthController:
    """Controller for authentication endpoints."""

    def __init__(self, service: AuthService) -> None:
        self._service = service

    async def login(self, payload: LoginRequest) -> LoginResponse:
        """Authenticate a user and return an access token."""
        try:
            return await self._service.login(payload)
        except InvalidCredentialsError:
            logger.warning(log.LOG_LOGIN_FAILED, payload.email)
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=err.ERR_INVALID_CREDENTIALS,
            )

    async def get_me(self, user_id: str) -> UserResponse:
        """Get the current authenticated user's profile."""
        return await self._service.get_current_user(user_id)

    async def logout(self) -> dict:
        """Logout the current user."""
        return {"message": "Logged out successfully"}
