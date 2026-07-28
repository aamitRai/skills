"""
Quote API schemas.

Pydantic models for quote request/response.
"""

from pydantic import BaseModel, Field


class QuoteCreateRequest(BaseModel):
    """Incoming payload to create a quote."""

    text: str = Field(..., min_length=1, max_length=1000)
    author: str = Field(default="", max_length=200)


class QuoteResponse(BaseModel):
    """Outgoing quote payload."""

    id: str
    text: str
    author: str
