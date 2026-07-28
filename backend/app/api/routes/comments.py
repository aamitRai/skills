"""
Comment route handlers.

HTTP endpoints for skill comment CRUD operations.
"""

from fastapi import APIRouter, Depends, status

from app.controllers.comment_controller import CommentController
from app.dependencies import get_comment_controller
from app.schemas.comment_schemas import (
    CommentCreateRequest,
    CommentResponse,
)
from fastapi.responses import Response

router = APIRouter(tags=["comments"])


@router.get(
    "/api/skills/{skill_id}/comments",
    response_model=list[CommentResponse],
    status_code=status.HTTP_200_OK,
)
async def list_comments(
    skill_id: str,
    controller: CommentController = Depends(get_comment_controller),
) -> list[CommentResponse]:
    """Get all comments for a skill."""
    return await controller.list_by_skill_id(skill_id)


@router.post(
    "/api/skills/{skill_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    payload: CommentCreateRequest,
    skill_id: str,
    controller: CommentController = Depends(get_comment_controller),
) -> CommentResponse:
    """Create a new comment on a skill."""
    return await controller.create(skill_id, payload)


@router.delete(
    "/api/skills/{skill_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    skill_id: str,
    comment_id: str,
    controller: CommentController = Depends(get_comment_controller),
) -> Response:
    """Delete a comment."""
    return await controller.delete(comment_id)
