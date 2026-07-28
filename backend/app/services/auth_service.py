"""Auth service."""

import logging

from app.constants import log_messages as log
from app.core.security import create_access_token, hash_password, verify_password
from app.exceptions.app_exceptions import (
    InvalidCredentialsError,
    UserNotFoundError,
)
from app.models.user import UserInDB
from app.repositories.settings_repository import SettingsRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import (
    LoginRequest,
    LoginResponse,
    SettingsResponse,
    SettingsUpdateRequest,
    UserCreateRequest,
    UserResponse as UserResponseSchema,
    UserUpdateRequest,
)

logger = logging.getLogger(__name__)


class AuthService:
    """Business logic for authentication and user management."""

    def __init__(
        self,
        user_repo: UserRepository,
        settings_repo: SettingsRepository,
    ) -> None:
        self._user_repo = user_repo
        self._settings_repo = settings_repo

    async def login(self, payload: LoginRequest) -> LoginResponse:
        """Authenticate a user and return an access token.

        Args:
            payload: Login credentials from the client.

        Returns:
            LoginResponse with token and user summary.

        Raises:
            InvalidCredentialsError: If email or password is wrong.
        """
        user = await self._user_repo.find_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.hashed_password):
            logger.warning(log.LOG_LOGIN_FAILED, payload.email)
            raise InvalidCredentialsError("Invalid email or password")

        token = create_access_token(data={"sub": str(user.id), "email": user.email})
        logger.info(log.LOG_USER_LOGGED_IN, user.id)
        return LoginResponse(
            access_token=token,
            user=UserResponseSchema(
                id=str(user.id),
                email=user.email,
                name=user.name,
                title=user.title,
                avatar_url=user.avatar_url,
            ),
        )

    async def get_current_user(self, user_id: str) -> UserResponseSchema:
        """Get the current authenticated user's profile.

        Args:
            user_id: The authenticated user's ID.

        Returns:
            UserResponseSchema with profile data.

        Raises:
            UserNotFoundError: If the user doesn't exist.
        """
        user = await self._user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User {user_id} not found")
        return UserResponseSchema(
            id=str(user.id),
            email=user.email,
            name=user.name,
            title=user.title,
            avatar_url=user.avatar_url,
        )

    async def update_profile(
        self, user_id: str, payload: UserUpdateRequest
    ) -> UserResponseSchema:
        """Update the current user's profile fields.

        Args:
            user_id: The authenticated user's ID.
            payload: Fields to update.

        Returns:
            Updated UserResponseSchema.

        Raises:
            UserNotFoundError: If the user doesn't exist.
        """
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_current_user(user_id)

        user = await self._user_repo.update(user_id, update_data)
        if user is None:
            raise UserNotFoundError(f"User {user_id} not found")
        logger.info(log.LOG_PROFILE_UPDATED, user_id)
        return UserResponseSchema(
            id=str(user.id),
            email=user.email,
            name=user.name,
            title=user.title,
            avatar_url=user.avatar_url,
        )

    async def get_settings(self, user_id: str) -> SettingsResponse:
        """Get settings for the current user.

        Args:
            user_id: The authenticated user's ID.

        Returns:
            SettingsResponse with current preferences.
        """
        settings = await self._settings_repo.find_by_user_id(user_id)
        if settings is None:
            settings = await self._settings_repo.upsert(user_id)
        return SettingsResponse(
            theme=settings.theme,
            remember=settings.remember,
        )

    async def update_settings(
        self, user_id: str, payload: SettingsUpdateRequest
    ) -> SettingsResponse:
        """Update settings for the current user.

        Args:
            user_id: The authenticated user's ID.
            payload: Settings fields to update.

        Returns:
            Updated SettingsResponse.
        """
        settings = await self._settings_repo.upsert(
            user_id,
            theme=payload.theme,
            remember=payload.remember,
        )
        logger.info(log.LOG_SETTINGS_UPDATED, user_id)
        return SettingsResponse(
            theme=settings.theme,
            remember=settings.remember,
        )

    async def register(self, payload: UserCreateRequest) -> UserResponseSchema:
        """Register a new user account.

        Args:
            payload: User registration data.

        Returns:
            UserResponseSchema for the created user.

        Raises:
            InvalidCredentialsError: If email already exists.
        """
        existing = await self._user_repo.find_by_email(payload.email)
        if existing:
            raise InvalidCredentialsError("Email already registered")

        user = UserInDB(
            email=payload.email,
            name=payload.name,
            title=payload.title,
            hashed_password=hash_password(payload.password),
        )
        created = await self._user_repo.create(user)
        logger.info(log.LOG_USER_REGISTERED, created.id)
        return UserResponseSchema(
            id=str(created.id),
            email=created.email,
            name=created.name,
            title=created.title,
            avatar_url=created.avatar_url,
        )
