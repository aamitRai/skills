"""
Quote route handlers.

HTTP endpoints for quote management and daily quote selection.
"""

from fastapi import APIRouter, Depends, status

from app.controllers.quote_controller import QuoteController
from app.dependencies import get_quote_controller
from app.schemas.quote_schemas import QuoteCreateRequest, QuoteResponse

router = APIRouter(prefix="/api/quotes", tags=["quotes"])


@router.get("/", response_model=QuoteResponse | None, status_code=status.HTTP_200_OK)
async def get_random_quote(
    controller: QuoteController = Depends(get_quote_controller),
) -> QuoteResponse | None:
    """Get a random quote from the database."""
    return await controller.get_today()


@router.get(
    "/today",
    response_model=QuoteResponse | None,
    status_code=status.HTTP_200_OK,
)
async def get_today_quote(
    controller: QuoteController = Depends(get_quote_controller),
) -> QuoteResponse | None:
    """Get a random quote for today's display (alias for /)."""
    return await controller.get_today()


@router.post("/", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_quote(
    payload: QuoteCreateRequest,
    controller: QuoteController = Depends(get_quote_controller),
) -> QuoteResponse:
    """Create a new quote."""
    return await controller.create(payload)
