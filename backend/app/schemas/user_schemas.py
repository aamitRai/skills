"""
User API schemas.

Pydantic models for request validation and response serialization.
Separate input/output models per standard §22.
"""

from pydantic import BaseModel, EmailStr, Field


# --- Auth ---

class LoginRequest(BaseModel):
    """Incoming payload for user login."""

    email: EmailStr
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    """Response after successful login."""

    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


# --- User Profile ---

class UserCreateRequest(BaseModel):
    """Incoming payload to create a new user."""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)
    title: str = Field(default="", max_length=200)


class UserUpdateRequest(BaseModel):
    """Incoming payload for partial user profile update."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    title: str | None = Field(default=None, max_length=200)


class UserResponse(BaseModel):
    """Outgoing user profile payload."""

    id: str
    email: str
    name: str
    title: str
    avatar_url: str | None = None


# --- Settings ---

class SettingsUpdateRequest(BaseModel):
    """Incoming payload to update user settings."""

    theme: str | None = None
    remember: bool | None = None


class SettingsResponse(BaseModel):
    """Outgoing settings payload."""

    theme: str
    remember: bool
