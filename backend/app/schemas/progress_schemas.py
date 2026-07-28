"""
Progress API schemas.

Pydantic models for skill progress request/response.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class ProgressUpdateRequest(BaseModel):
    """Incoming payload to update skill progress."""

    progress: int = Field(..., ge=0, le=100)


class ProgressResponse(BaseModel):
    """Outgoing progress payload."""

    skill_id: str
    progress: int
    status: str
    last_updated: datetime
