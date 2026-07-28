"""Comment service."""

import logging

from app.constants import log_messages as log
from app.exceptions.app_exceptions import CommentNotFoundError
from app.models.comment import CommentInDB
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment_schemas import (
    CommentCreateRequest,
    CommentResponse,
)

logger = logging.getLogger(__name__)


class CommentService:
    """Business logic for comment management."""

    def __init__(self, comment_repo: CommentRepository) -> None:
        self._comment_repo = comment_repo

    async def get_by_skill_id(self, skill_id: str) -> list[CommentResponse]:
        """Get all comments for a skill.

        Args:
            skill_id: The skill's ID.

        Returns:
            List of CommentResponse sorted by creation time.
        """
        comments = await self._comment_repo.find_by_skill_id(skill_id)
        return [
            CommentResponse(
                id=str(c.id),
                skill_id=c.skill_id,
                text=c.text,
                created_at=c.created_at,
            )
            for c in comments
        ]

    async def create(
        self, skill_id: str, payload: CommentCreateRequest
    ) -> CommentResponse:
        """Create a new comment on a skill.

        Args:
            skill_id: The skill's ID.
            payload: Comment text.

        Returns:
            CommentResponse for the created comment.
        """
        comment = CommentInDB(
            skill_id=skill_id,
            text=payload.text,
        )
        created = await self._comment_repo.create(comment)
        logger.info(log.LOG_COMMENT_CREATED, created.id)
        return CommentResponse(
            id=str(created.id),
            skill_id=created.skill_id,
            text=created.text,
            created_at=created.created_at,
        )

    async def delete(self, comment_id: str) -> None:
        """Delete a comment.

        Args:
            comment_id: The comment ID.

        Raises:
            CommentNotFoundError: If the comment doesn't exist.
        """
        comment = await self._comment_repo.find_by_id(comment_id)
        if comment is None:
            raise CommentNotFoundError(f"Comment {comment_id} not found")

        deleted = await self._comment_repo.delete(comment_id)
        if not deleted:
            raise CommentNotFoundError(f"Comment {comment_id} not found")
        logger.info(log.LOG_COMMENT_DELETED, comment_id)
