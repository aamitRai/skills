"""
Comment API schemas.

Pydantic models for comment CRUD request/response.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class CommentCreateRequest(BaseModel):
    """Incoming payload to create a comment on a skill."""

    text: str = Field(..., min_length=1, max_length=2000)


class CommentResponse(BaseModel):
    """Outgoing comment payload."""

    id: str
    skill_id: str
    text: str
    created_at: datetime
