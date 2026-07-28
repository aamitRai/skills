"""Quote Beanie document model."""

from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Quote(Document):
    """Quote document."""

    text: str
    author: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "quotes"


# Alias for service-layer naming convention
QuoteInDB = Quote
