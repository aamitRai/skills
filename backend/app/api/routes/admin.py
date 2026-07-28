"""
Admin and bootstrap route handlers.

HTTP endpoints for seed data import and admin operations.
"""

from fastapi import APIRouter, Depends, status

from app.controllers.admin_controller import AdminController
from app.dependencies import get_admin_controller

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/bootstrap", status_code=status.HTTP_200_OK)
async def bootstrap(
    controller: AdminController = Depends(get_admin_controller),
) -> dict:
    """
    Import seed data from public/data JSON files.

    Idempotent operation — safe to call multiple times.
    Creates the default user, categories, skills, and quotes.
    """
    return await controller.bootstrap()
