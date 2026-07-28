"""Quote service."""

import logging

from app.constants import log_messages as log
from app.models.quote import QuoteInDB
from app.repositories.quote_repository import QuoteRepository
from app.schemas.quote_schemas import QuoteCreateRequest, QuoteResponse

logger = logging.getLogger(__name__)


class QuoteService:
    """Business logic for quote management."""

    def __init__(self, quote_repo: QuoteRepository) -> None:
        self._quote_repo = quote_repo

    async def get_all(self) -> list[QuoteResponse]:
        """Get all quotes.

        Returns:
            List of QuoteResponse.
        """
        quotes = await self._quote_repo.find_all()
        return [
            QuoteResponse(id=str(q.id), text=q.text, author=q.author)
            for q in quotes
        ]

    async def get_today(self) -> QuoteResponse | None:
        """Get a random quote for today's display.

        Returns:
            QuoteResponse or None if no quotes exist.
        """
        quote = await self._quote_repo.find_random()
        if quote is None:
            return None
        return QuoteResponse(id=str(quote.id), text=quote.text, author=quote.author)

    async def create(self, payload: QuoteCreateRequest) -> QuoteResponse:
        """Create a new quote.

        Args:
            payload: Quote creation data.

        Returns:
            QuoteResponse for the created quote.
        """
        quote = QuoteInDB(
            text=payload.text,
            author=payload.author,
        )
        created = await self._quote_repo.create(quote)
        logger.info("Quote created", extra={"quote_id": created.id})
        return QuoteResponse(
            id=str(created.id),
            text=created.text,
            author=created.author,
        )

    async def bulk_import(self, quotes_data: list[dict]) -> int:
        """Bulk import quotes from seed data.

        Args:
            quotes_data: List of dictionaries with 'text' and 'author' keys.

        Returns:
            Number of quotes inserted.
        """
        quotes = [
            QuoteInDB(text=q.get("text", ""), author=q.get("author", ""))
            for q in quotes_data
        ]
        count = await self._quote_repo.bulk_insert(quotes)
        logger.info(log.LOG_BOOTSTRAP_QUOTES_IMPORTED, count)
        return count
