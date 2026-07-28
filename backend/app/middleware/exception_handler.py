"""Exception handler middleware.

Centralized exception handlers for all known application error types.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.constants.http_status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from app.exceptions.app_exceptions import (
    AppError,
    CategoryNotFoundError,
    CommentNotFoundError,
    DuplicateError,
    InvalidCredentialsError,
    SkillNotFoundError,
    TokenError,
    UserNotFoundError,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register centralized exception handlers for known error types.

    Args:
        app: FastAPI application instance.
    """

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(
        request: Request, exc: InvalidCredentialsError
    ) -> JSONResponse:
        logger.warning("Authentication failed", extra={"path": request.url.path})
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"error": "invalid_credentials", "message": str(exc)},
        )

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(
        request: Request, exc: UserNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"error": "user_not_found", "message": str(exc)},
        )

    @app.exception_handler(TokenError)
    async def token_error_handler(
        request: Request, exc: TokenError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"error": "token_error", "message": str(exc)},
        )

    @app.exception_handler(DuplicateError)
    async def duplicate_handler(
        request: Request, exc: DuplicateError
    ) -> JSONResponse:
        logger.warning("Duplicate resource", extra={"path": request.url.path})
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"error": "duplicate", "message": str(exc)},
        )

    @app.exception_handler(CategoryNotFoundError)
    async def category_not_found_handler(
        request: Request, exc: CategoryNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"error": "category_not_found", "message": str(exc)},
        )

    @app.exception_handler(SkillNotFoundError)
    async def skill_not_found_handler(
        request: Request, exc: SkillNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"error": "skill_not_found", "message": str(exc)},
        )

    @app.exception_handler(CommentNotFoundError)
    async def comment_not_found_handler(
        request: Request, exc: CommentNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"error": "comment_not_found", "message": str(exc)},
        )

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        logger.error("Application error", extra={"path": request.url.path})
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "application_error", "message": str(exc)},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.critical(
            "Unhandled exception",
            exc_info=True,
            extra={"path": request.url.path},
        )
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "internal_error",
                "message": "An unexpected error occurred",
            },
        )
