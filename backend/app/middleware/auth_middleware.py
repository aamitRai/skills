"""Authentication middleware utilities.

Provides the get_current_user_id dependency for extracting and validating
JWT tokens from the Authorization header.
"""

from fastapi import Header, HTTPException

from app.constants.http_status import HTTP_401_UNAUTHORIZED
from app.core.security import decode_access_token
from app.exceptions.app_exceptions import TokenError


def get_current_user_id(authorization: str = Header(default=None)) -> str:
    """
    Extract and validate the current user ID from the Authorization header.

    Args:
        authorization: Bearer token string from the request header.

    Returns:
        The user ID from the token payload.

    Raises:
        HTTPException: If the token is missing or invalid.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )
    try:
        token = authorization.split(" ", 1)[1]
        payload = decode_access_token(token)
        user_id = str(payload.get("sub", ""))
        if not user_id:
            raise TokenError("Invalid token payload")
        return user_id
    except TokenError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    except Exception:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Failed to decode token",
        )
