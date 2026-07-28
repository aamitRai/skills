"""Comment Beanie document model."""

from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Comment(Document):
    """Comment on a skill."""

    skill_id: str = Field(index=True)
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "comments"
        indexes = [
            [
                ("skill_id", 1),
            ],
        ]


# Alias for service-layer naming convention
CommentInDB = Comment
