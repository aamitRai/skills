"""Comment repository — Beanie async data access."""

import logging

from app.models.comment import Comment

logger = logging.getLogger(__name__)


class CommentRepository:
    """Data access layer for comment documents."""

    async def find_by_skill_id(self, skill_id: str) -> list[Comment]:
        """Find all comments for a specific skill."""
        cursor = Comment.find(Comment.skill_id == skill_id).sort(-Comment.created_at)
        return await cursor.to_list()

    async def find_by_id(self, comment_id: str) -> Comment | None:
        """Find a single comment by ID."""
        return await Comment.get(comment_id)

    async def create(self, comment: Comment) -> Comment:
        """Insert a new comment document."""
        await comment.create()
        logger.info("Comment created", extra={"comment_id": str(comment.id)})
        return comment

    async def delete(self, comment_id: str) -> bool:
        """Remove a comment document."""
        comment = await self.find_by_id(comment_id)
        if comment is None:
            return False
        await comment.delete()
        return True

    async def delete_by_skill_id(self, skill_id: str) -> int:
        """Delete all comments for a skill."""
        comments = await self.find_by_skill_id(skill_id)
        for comment in comments:
            await comment.delete()
        return len(comments)
