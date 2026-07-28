"""Quote controller — HTTP-level handling for quote endpoints."""

import logging

from app.schemas.quote_schemas import QuoteCreateRequest, QuoteResponse
from app.services.quote_service import QuoteService

logger = logging.getLogger(__name__)


class QuoteController:
    """Controller for quote endpoints."""

    def __init__(self, service: QuoteService) -> None:
        self._service = service

    async def list_all(self) -> list[QuoteResponse]:
        """GET /quotes — Get all quotes."""
        return await self._service.get_all()

    async def get_today(self) -> QuoteResponse | None:
        """GET /quotes/today — Get a random quote for today."""
        return await self._service.get_today()

    async def create(self, payload: QuoteCreateRequest) -> QuoteResponse:
        """POST /quotes — Create a new quote."""
        return await self._service.create(payload)
