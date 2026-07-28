"""
Skill route handlers.

HTTP endpoints for skill CRUD within categories.
"""

from fastapi import APIRouter, Depends, status

from app.controllers.skill_controller import SkillController
from app.dependencies import get_skill_controller
from app.schemas.category_schemas import (
    SkillCreateRequest,
    SkillMoveRequest,
    SkillResponse,
    SkillUpdateRequest,
)
from fastapi.responses import Response

router = APIRouter(tags=["skills"])


@router.post(
    "/api/categories/{category_id}/skills",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_skill(
    payload: SkillCreateRequest,
    category_id: str,
    controller: SkillController = Depends(get_skill_controller),
) -> SkillResponse:
    """Add a new skill to a category."""
    return await controller.create(category_id, payload)


@router.get("/api/skills/{skill_id}", response_model=SkillResponse, status_code=status.HTTP_200_OK)
async def get_skill(
    skill_id: str,
    controller: SkillController = Depends(get_skill_controller),
) -> SkillResponse:
    """Get a single skill by ID."""
    return await controller.get_by_id(skill_id)


@router.patch("/api/skills/{skill_id}", response_model=SkillResponse, status_code=status.HTTP_200_OK)
async def update_skill(
    payload: SkillUpdateRequest,
    skill_id: str,
    controller: SkillController = Depends(get_skill_controller),
) -> SkillResponse:
    """Update a skill's fields."""
    return await controller.update(skill_id, payload)


@router.delete("/api/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: str,
    controller: SkillController = Depends(get_skill_controller),
) -> Response:
    """Delete a skill and cascade delete its progress and comments."""
    return await controller.delete(skill_id)


@router.patch("/api/skills/{skill_id}/move", status_code=status.HTTP_200_OK)
async def move_skill(
    payload: SkillMoveRequest,
    skill_id: str,
    controller: SkillController = Depends(get_skill_controller),
) -> dict:
    """Move a skill up or down in display order within its category."""
    return await controller.move(skill_id, payload)
