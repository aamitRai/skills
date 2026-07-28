"""
Dependency injection factories.

FastAPI Depends() factories for repositories, services, and controllers.
All database operations use Beanie ODM (MongoDB).
"""

from fastapi import Depends

from app.repositories.user_repository import UserRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.progress_repository import ProgressRepository
from app.repositories.comment_repository import CommentRepository
from app.repositories.quote_repository import QuoteRepository
from app.repositories.settings_repository import SettingsRepository
from app.services.auth_service import AuthService
from app.services.category_service import CategoryService
from app.services.progress_service import ProgressService
from app.services.comment_service import CommentService
from app.services.dashboard_service import DashboardService
from app.services.quote_service import QuoteService
from app.controllers.auth_controller import AuthController
from app.controllers.user_controller import UserController
from app.controllers.category_controller import CategoryController
from app.controllers.skill_controller import SkillController
from app.controllers.progress_controller import ProgressController
from app.controllers.comment_controller import CommentController
from app.controllers.dashboard_controller import DashboardController
from app.controllers.quote_controller import QuoteController
from app.controllers.admin_controller import AdminController


# --- Repository instances (Beanie ODM — no session needed) ---

async def get_user_repository() -> UserRepository:
    """Create UserRepository instance."""
    return UserRepository()


async def get_category_repository() -> CategoryRepository:
    """Create CategoryRepository instance."""
    return CategoryRepository()


async def get_progress_repository() -> ProgressRepository:
    """Create ProgressRepository instance."""
    return ProgressRepository()


async def get_comment_repository() -> CommentRepository:
    """Create CommentRepository instance."""
    return CommentRepository()


async def get_quote_repository() -> QuoteRepository:
    """Create QuoteRepository instance."""
    return QuoteRepository()


async def get_settings_repository() -> SettingsRepository:
    """Create SettingsRepository instance."""
    return SettingsRepository()


# --- Service instances ---

async def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    settings_repo: SettingsRepository = Depends(get_settings_repository),
) -> AuthService:
    """Create AuthService instance."""
    return AuthService(user_repo, settings_repo)


async def get_category_service(
    category_repo: CategoryRepository = Depends(get_category_repository),
    progress_repo: ProgressRepository = Depends(get_progress_repository),
    comment_repo: CommentRepository = Depends(get_comment_repository),
) -> CategoryService:
    """Create CategoryService instance."""
    return CategoryService(category_repo, progress_repo, comment_repo)


async def get_progress_service(
    progress_repo: ProgressRepository = Depends(get_progress_repository),
) -> ProgressService:
    """Create ProgressService instance."""
    return ProgressService(progress_repo)


async def get_comment_service(
    comment_repo: CommentRepository = Depends(get_comment_repository),
) -> CommentService:
    """Create CommentService instance."""
    return CommentService(comment_repo)


async def get_dashboard_service(
    category_repo: CategoryRepository = Depends(get_category_repository),
    progress_repo: ProgressRepository = Depends(get_progress_repository),
    comment_repo: CommentRepository = Depends(get_comment_repository),
) -> DashboardService:
    """Create DashboardService instance."""
    return DashboardService(category_repo, progress_repo, comment_repo)


async def get_quote_service(
    quote_repo: QuoteRepository = Depends(get_quote_repository),
) -> QuoteService:
    """Create QuoteService instance."""
    return QuoteService(quote_repo)


# --- Controller instances ---

async def get_auth_controller(
    service: AuthService = Depends(get_auth_service),
) -> AuthController:
    """Create AuthController instance."""
    return AuthController(service=service)


async def get_user_controller(
    service: AuthService = Depends(get_auth_service),
) -> UserController:
    """Create UserController instance."""
    return UserController(service=service)


async def get_category_controller(
    service: CategoryService = Depends(get_category_service),
) -> CategoryController:
    """Create CategoryController instance."""
    return CategoryController(service=service)


async def get_skill_controller(
    service: CategoryService = Depends(get_category_service),
) -> SkillController:
    """Create SkillController instance."""
    return SkillController(service=service)


async def get_progress_controller(
    service: ProgressService = Depends(get_progress_service),
) -> ProgressController:
    """Create ProgressController instance."""
    return ProgressController(service=service)


async def get_comment_controller(
    service: CommentService = Depends(get_comment_service),
) -> CommentController:
    """Create CommentController instance."""
    return CommentController(service=service)


async def get_dashboard_controller(
    service: DashboardService = Depends(get_dashboard_service),
) -> DashboardController:
    """Create DashboardController instance."""
    return DashboardController(service=service)


async def get_quote_controller(
    service: QuoteService = Depends(get_quote_service),
) -> QuoteController:
    """Create QuoteController instance."""
    return QuoteController(service=service)


async def get_admin_controller(
    auth_service: AuthService = Depends(get_auth_service),
    category_service: CategoryService = Depends(get_category_service),
    quote_service: QuoteService = Depends(get_quote_service),
) -> AdminController:
    """Create AdminController instance."""
    return AdminController(
        auth_service=auth_service,
        category_service=category_service,
        quote_service=quote_service,
    )
