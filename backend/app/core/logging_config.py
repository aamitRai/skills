"""
Structured JSON logging configuration.

Configures application-wide logging with JSON-formatted output for
machine-parseable log aggregation. Also configures uvicorn loggers
so server-level logs appear alongside application logs.
"""

import json
import logging
import sys
from datetime import datetime, timezone
from logging import LogRecord


class JsonFormatter(logging.Formatter):
    """Formats log records as JSON for structured log aggregation."""

    def format(self, record: LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info and record.exc_info[0] is not None:
            log_obj["exception"] = self.formatException(record.exc_info)
        for key, value in record.__dict__.items():
            if key not in {
                *logging.LogRecord.__dict__.keys(),
                "trace_id",
            } and not key.startswith("_"):
                log_obj[key] = value
        return json.dumps(log_obj, default=str)


def configure_logging(level: str = "INFO") -> None:
    """
    Configure root logger with JSON formatter.

    Also configures uvicorn loggers so server-level logs (requests,
    startup/shutdown messages) appear in the same output stream.

    Args:
        level: Logging level string (DEBUG, INFO, WARNING, ERROR).
    """
    formatter = JsonFormatter()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Root logger (application logs)
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.handlers = [handler]

    # Uvicorn loggers (server-level logs: requests, startup, shutdown)
    for uvicorn_logger in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        logger = logging.getLogger(uvicorn_logger)
        logger.handlers = []  # Remove default handlers to avoid duplicates
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
