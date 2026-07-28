"""FastAPI application factory."""

import logging

from fastapi import FastAPI

from app.api.routes import (
    admin_router,
    auth_router,
    categories_router,
    comments_router,
    dashboard_router,
    progress_router,
    quotes_router,
    skills_router,
    users_router,
)
from app.core.config import settings
from app.core.database import close_db, init_db
from app.core.logging_config import configure_logging
from app.middleware.cors_middleware import add_cors_middleware
from app.middleware.exception_handler import register_exception_handlers

configure_logging(level="DEBUG" if settings.DEBUG else "INFO")
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Backend API for the Skills Tracker application",
    )

    add_cors_middleware(app)
    register_exception_handlers(app)

    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(categories_router)
    app.include_router(skills_router)
    app.include_router(progress_router)
    app.include_router(comments_router)
    app.include_router(dashboard_router)
    app.include_router(quotes_router)
    app.include_router(admin_router)

    @app.on_event("startup")
    async def startup() -> None:
        await init_db()
        logger.info("Application started")

    @app.on_event("shutdown")
    async def shutdown() -> None:
        await close_db()
        logger.info("Application shutting down")

    @app.get("/health", status_code=200)
    async def health_check() -> dict:
        return {"status": "healthy", "version": settings.APP_VERSION}

    return app


# Create the application instance
app = create_app()
