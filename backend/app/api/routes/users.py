"""
User profile route handlers.

HTTP endpoints for profile updates and settings management.
"""

from fastapi import APIRouter, Depends, status

from app.controllers.user_controller import UserController
from app.dependencies import get_user_controller
from app.middleware.auth_middleware import get_current_user_id
from app.schemas.user_schemas import (
    SettingsResponse,
    SettingsUpdateRequest,
    UserResponse,
    UserUpdateRequest,
)

router = APIRouter(prefix="/api/users/me", tags=["users"])


@router.get("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_profile(
    user_id: str = Depends(get_current_user_id),
    controller: UserController = Depends(get_user_controller),
) -> UserResponse:
    """Get the current user's full profile."""
    return await controller.get_profile(user_id)


@router.patch("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_profile(
    payload: UserUpdateRequest,
    user_id: str = Depends(get_current_user_id),
    controller: UserController = Depends(get_user_controller),
) -> UserResponse:
    """Update the current user's profile fields."""
    return await controller.update_profile(user_id, payload)


@router.get(
    "/settings", response_model=SettingsResponse, status_code=status.HTTP_200_OK
)
async def get_settings(
    user_id: str = Depends(get_current_user_id),
    controller: UserController = Depends(get_user_controller),
) -> SettingsResponse:
    """Get the current user's settings."""
    return await controller.get_settings(user_id)


@router.patch(
    "/settings", response_model=SettingsResponse, status_code=status.HTTP_200_OK
)
async def update_settings(
    payload: SettingsUpdateRequest,
    user_id: str = Depends(get_current_user_id),
    controller: UserController = Depends(get_user_controller),
) -> SettingsResponse:
    """Update the current user's settings."""
    return await controller.update_settings(user_id, payload)
