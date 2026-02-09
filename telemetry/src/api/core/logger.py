"""Structured logging configuration.

This module configures structured logging with OpenTelemetry integration.
Follows the pattern from grassroots project logger.py.
"""

import logging
import os
import sys
from collections.abc import MutableMapping
from typing import Any

import structlog
from opentelemetry import trace


def add_opentelemetry_context(
    _logger: structlog.stdlib.BoundLogger,
    _method_name: str,
    event_dict: MutableMapping[str, Any],
) -> MutableMapping[str, Any]:
    """Add OpenTelemetry trace context to log records.

    Args:
        _logger: Structlog bound logger
        _method_name: Method name (unused)
        event_dict: Event dictionary to augment

    Returns:
        MutableMapping: Event dictionary with trace context
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        span_context = span.get_span_context()
        event_dict["trace_id"] = format(span_context.trace_id, "032x")
        event_dict["span_id"] = format(span_context.span_id, "016x")

    # Add service name from environment
    service_name = os.getenv("SERVICE_NAME", "telemetry-sample")
    event_dict["service_name"] = service_name

    return event_dict


def rename_event_to_message(
    _logger: structlog.stdlib.BoundLogger,
    _method_name: str,
    event_dict: MutableMapping[str, Any],
) -> MutableMapping[str, Any]:
    """Rename the 'event' key to 'message' for consistency with logging standards.

    Args:
        _logger: Structlog bound logger
        _method_name: Method name (unused)
        event_dict: Event dictionary

    Returns:
        MutableMapping: Event dictionary with renamed key
    """
    if "event" in event_dict:
        event_dict["message"] = event_dict.pop("event")
    return event_dict


def configure_logging() -> None:
    """Configure structured logging for the application.

    This function sets up:
    - Structlog with JSON rendering
    - OpenTelemetry trace context injection
    - ISO timestamp format
    - Exception formatting
    """
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            add_opentelemetry_context,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            rename_event_to_message,
            structlog.processors.JSONRenderer(ensure_ascii=False),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure Python logging - use plain formatter since structlog handles JSON
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))

    # Set logging level to INFO
    log_level = logging.INFO

    # Configure root logger
    logging.basicConfig(level=log_level, handlers=[handler], force=True)

    # Suppress noisy loggers
    logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
    logging.getLogger("azure.monitor.opentelemetry.exporter.export._base").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


# Flag to track if logging has been configured
_logging_configured = False


def get_logger(name: str | None) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance.

    This function automatically configures logging on first call.

    Args:
        name: Logger name (usually __name__)

    Returns:
        structlog.stdlib.BoundLogger: Configured logger
    """
    global _logging_configured
    if not _logging_configured:
        configure_logging()
        _logging_configured = True
    return structlog.get_logger(name)


def bind_context(**kwargs: str | float | bool | None) -> None:
    """Bind context variables to be included in all log messages.

    Args:
        **kwargs: Key-value pairs to bind to context

    Example:
        ```python
        bind_context(user_id="123", request_id="abc")
        logger.info("Processing request")  # Includes user_id and request_id
        ```
    """
    structlog.contextvars.bind_contextvars(**kwargs)


def clear_context() -> None:
    """Clear all bound context variables."""
    structlog.contextvars.clear_contextvars()
