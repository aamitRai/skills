"""
Authentication route handlers.

HTTP endpoints for login, logout, and current user retrieval.
"""

from fastapi import APIRouter, Depends, status

from app.controllers.auth_controller import AuthController
from app.dependencies import get_auth_controller
from app.middleware.auth_middleware import get_current_user_id
from app.schemas.user_schemas import LoginRequest, LoginResponse, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    payload: LoginRequest,
    controller: AuthController = Depends(get_auth_controller),
) -> LoginResponse:
    """Authenticate a user and return an access token."""
    return await controller.login(payload)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    _user_id: str = Depends(get_current_user_id),
    controller: AuthController = Depends(get_auth_controller),
) -> dict:
    """Logout the current user."""
    return await controller.logout()


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_me(
    user_id: str = Depends(get_current_user_id),
    controller: AuthController = Depends(get_auth_controller),
) -> UserResponse:
    """Get the current authenticated user's profile."""
    return await controller.get_me(user_id)
