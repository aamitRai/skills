"""
Category route handlers.

HTTP endpoints for category CRUD operations.
"""

from fastapi import APIRouter, Depends, status

from app.controllers.category_controller import CategoryController
from app.dependencies import get_category_controller
from app.middleware.auth_middleware import get_current_user_id
from app.schemas.category_schemas import (
    CategoryCreateRequest,
    CategoryResponse,
    CategoryUpdateRequest,
)
from fastapi.responses import Response

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def list_categories(
    user_id: str = Depends(get_current_user_id),
    controller: CategoryController = Depends(get_category_controller),
) -> list[CategoryResponse]:
    """Get all categories for the current user."""
    return await controller.list_all(user_id)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryCreateRequest,
    user_id: str = Depends(get_current_user_id),
    controller: CategoryController = Depends(get_category_controller),
) -> CategoryResponse:
    """Create a new category."""
    return await controller.create(user_id, payload)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_category(
    category_id: str,
    controller: CategoryController = Depends(get_category_controller),
) -> CategoryResponse:
    """Get a single category by ID."""
    return await controller.get_by_id(category_id)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
async def update_category(
    payload: CategoryUpdateRequest,
    category_id: str,
    controller: CategoryController = Depends(get_category_controller),
) -> CategoryResponse:
    """Update a category's fields."""
    return await controller.update(category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    controller: CategoryController = Depends(get_category_controller),
) -> Response:
    """Delete a category and cascade delete all related data."""
    return await controller.delete(category_id)
