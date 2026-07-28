"""
Progress route handlers.

HTTP endpoints for skill progress tracking.
"""

from fastapi import APIRouter, Depends, status

from app.controllers.progress_controller import ProgressController
from app.dependencies import get_progress_controller
from app.schemas.progress_schemas import ProgressResponse, ProgressUpdateRequest

router = APIRouter(tags=["progress"])


@router.get("/api/progress", response_model=list[ProgressResponse], status_code=status.HTTP_200_OK)
async def list_progress(
    controller: ProgressController = Depends(get_progress_controller),
) -> list[ProgressResponse]:
    """Get all progress records."""
    return await controller.list_all()


@router.get(
    "/api/skills/{skill_id}/progress",
    response_model=ProgressResponse,
    status_code=status.HTTP_200_OK,
)
async def get_skill_progress(
    skill_id: str,
    controller: ProgressController = Depends(get_progress_controller),
) -> ProgressResponse:
    """Get progress for a specific skill."""
    return await controller.get_by_skill_id(skill_id)


@router.put(
    "/api/skills/{skill_id}/progress",
    response_model=ProgressResponse,
    status_code=status.HTTP_200_OK,
)
async def update_skill_progress(
    payload: ProgressUpdateRequest,
    skill_id: str,
    controller: ProgressController = Depends(get_progress_controller),
) -> ProgressResponse:
    """Update progress for a skill."""
    return await controller.update(skill_id, payload)
