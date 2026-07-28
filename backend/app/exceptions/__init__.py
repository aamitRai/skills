"""Exceptions package."""

from app.exceptions.app_exceptions import (
    AppError,
    CategoryNotFoundError,
    CommentNotFoundError,
    InvalidCredentialsError,
    SkillNotFoundError,
    TokenError,
    UserNotFoundError,
)

__all__ = [
    "AppError",
    "CategoryNotFoundError",
    "CommentNotFoundError",
    "InvalidCredentialsError",
    "SkillNotFoundError",
    "TokenError",
    "UserNotFoundError",
]
