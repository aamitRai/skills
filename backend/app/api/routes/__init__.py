"""Route index — single import point for all routers."""

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.categories import router as categories_router
from app.api.routes.skills import router as skills_router
from app.api.routes.progress import router as progress_router
from app.api.routes.comments import router as comments_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.quotes import router as quotes_router
from app.api.routes.admin import router as admin_router

__all__ = [
    "auth_router",
    "users_router",
    "categories_router",
    "skills_router",
    "progress_router",
    "comments_router",
    "dashboard_router",
    "quotes_router",
    "admin_router",
]
