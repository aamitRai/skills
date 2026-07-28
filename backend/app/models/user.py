"""User Beanie document model."""

from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class User(Document):
    """User account document."""

    email: str = Field(index=True)
    name: str
    title: str = ""
    avatar_url: str | None = None
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"
        indexes = [
            [
                ("email", 1),
            ],
        ]


# Alias for service-layer naming convention
UserInDB = User
