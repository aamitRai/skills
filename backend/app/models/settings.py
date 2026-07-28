"""User settings Beanie document model."""

from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class UserSettings(Document):
    """User preferences document."""

    user_id: str = Field(index=True, unique=True)
    theme: str = "light"
    remember: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "user_settings"
        indexes = [
            [
                ("user_id", 1),
            ],
        ]
