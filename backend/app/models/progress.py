"""Skill progress Beanie document model."""

from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class SkillProgress(Document):
    """Progress record for a skill."""

    skill_id: str = Field(index=True, unique=True)
    progress: float = 0.0
    status: str = "not-started"
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "skill_progress"
        indexes = [
            [
                ("skill_id", 1),
            ],
        ]


# Alias for service-layer naming convention
SkillProgressInDB = SkillProgress
