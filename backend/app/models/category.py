"""Category and Skill Beanie document models."""

from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Skill(Document):
    """Skill document — belongs to a category."""

    category_id: str = Field(index=True)
    name: str
    index: int = 0
    priority: str = "medium"
    difficulty: str = "medium"
    estimated_hours: int | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "skills"
        indexes = [
            [
                ("category_id", 1),
            ],
        ]


class Category(Document):
    """Category document."""

    user_id: str = Field(index=True)
    name: str
    icon: str = "📁"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "categories"
        indexes = [
            [
                ("user_id", 1),
            ],
        ]


# Aliases for service-layer naming convention
CategoryInDB = Category
SkillInDB = Skill
