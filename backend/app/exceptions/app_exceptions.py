"""Application-wide exception classes."""


class AppError(Exception):
    """Base application exception."""


class InvalidCredentialsError(AppError):
    """Invalid login credentials."""


class UserNotFoundError(AppError):
    """User not found."""


class TokenError(AppError):
    """Token creation or validation failed."""


class CategoryNotFoundError(AppError):
    """Category not found."""


class SkillNotFoundError(AppError):
    """Skill not found."""


class CommentNotFoundError(AppError):
    """Comment not found."""


class DuplicateError(AppError):
    """A resource with the same name already exists."""
