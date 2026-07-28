"""Admin controller — HTTP-level handling for admin endpoints."""

import json
import logging
from pathlib import Path

from app.constants import log_messages as log
from app.exceptions.app_exceptions import InvalidCredentialsError
from app.repositories.user_repository import UserRepository
from app.schemas.category_schemas import CategoryCreateRequest, SkillCreateRequest
from app.schemas.user_schemas import UserCreateRequest
from app.services.auth_service import AuthService
from app.services.category_service import CategoryService
from app.services.quote_service import QuoteService

logger = logging.getLogger(__name__)

_SEED_DATA_DIR = Path(__file__).parents[2] / "public" / "data"


class AdminController:
    """Controller for admin endpoints."""

    def __init__(
        self,
        auth_service: AuthService,
        category_service: CategoryService,
        quote_service: QuoteService,
    ) -> None:
        self._auth_service = auth_service
        self._category_service = category_service
        self._quote_service = quote_service
        self._user_repo = UserRepository()

    async def bootstrap(self) -> dict:
        """Import seed data from public/data JSON files.

        Idempotent operation — safe to call multiple times.
        """
        result = {
            "user_created": False,
            "categories_imported": 0,
            "skills_imported": 0,
            "quotes_imported": 0,
        }

        try:
            user = await self._auth_service.register(
                UserCreateRequest(
                    email="user@skills.app",
                    name="Skill User",
                    password="password123",
                    title="Developer",
                )
            )
            result["user_created"] = True
            user_id = user.id
            logger.info(log.LOG_BOOTSTRAP_USER_CREATED, user_id)
        except InvalidCredentialsError:
            existing = await self._user_repo.find_by_email("user@skills.app")
            user_id = existing.id if existing else "unknown"
            logger.info(log.LOG_BOOTSTRAP_USER_CREATED, user_id)

        categories_path = _SEED_DATA_DIR / "categories.json"
        if categories_path.exists():
            try:
                categories_data = json.loads(categories_path.read_text(encoding="utf-8"))
                cats_count = 0
                skills_count = 0
                for cat_data in categories_data.get("categories", []):
                    cat = await self._category_service.create(
                        user_id,
                        CategoryCreateRequest(
                            name=cat_data["name"],
                            icon=cat_data.get("icon", "📁"),
                        ),
                    )
                    cats_count += 1
                    for skill_data in cat_data.get("skills", []):
                        await self._category_service.add_skill(
                            cat.id,
                            SkillCreateRequest(
                                name=skill_data["name"],
                                priority=skill_data.get("priority", "medium"),
                                difficulty=skill_data.get("difficulty", "medium"),
                                estimated_hours=skill_data.get("estimatedHours"),
                            ),
                        )
                        skills_count += 1
                result["categories_imported"] = cats_count
                result["skills_imported"] = skills_count
                logger.info(log.LOG_BOOTSTRAP_CATEGORIES_IMPORTED, cats_count)
                logger.info(log.LOG_BOOTSTRAP_SKILLS_IMPORTED, skills_count)
            except Exception as exc:
                logger.error(log.LOG_BOOTSTRAP_FAILED, str(exc), exc_info=True)

        quotes_path = _SEED_DATA_DIR / "quotes.json"
        if quotes_path.exists():
            try:
                quotes_data = json.loads(quotes_path.read_text(encoding="utf-8"))
                count = await self._quote_service.bulk_import(quotes_data)
                result["quotes_imported"] = count
                logger.info(log.LOG_BOOTSTRAP_QUOTES_IMPORTED, count)
            except Exception as exc:
                logger.error(log.LOG_BOOTSTRAP_FAILED, str(exc), exc_info=True)

        return result
