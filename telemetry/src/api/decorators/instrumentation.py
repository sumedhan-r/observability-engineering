"""Instrumentation utilities and decorators.

This module provides utilities for manual instrumentation of code with OpenTelemetry.
Follows the pattern from grassroots project tracer.py.
"""

import functools
import inspect
from contextlib import contextmanager
from typing import Any, Callable

from opentelemetry import trace
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Status, StatusCode, Tracer

from src.api.core.logger import get_logger

logger = get_logger(__name__)

# Global tracer instance
_tracer: Tracer | None = None


def set_global_tracer(tracer: Tracer) -> None:
    """Set the global tracer instance.

    This should be called once during application startup.

    Args:
        tracer: OpenTelemetry tracer instance
    """
    global _tracer
    _tracer = tracer


def get_tracer() -> Tracer:
    """Get the global tracer instance.

    Returns:
        Tracer: OpenTelemetry tracer

    Raises:
        RuntimeError: If tracer not initialized
    """
    if _tracer is None:
        raise RuntimeError("Tracer not initialized. Call set_global_tracer() first.")
    return _tracer


def instrument(
    _func: Callable | None = None,
    *,
    span_name: str = "",
    record_exception: bool = True,
    attributes: dict[str, str] | None = None,
    existing_tracer: Tracer | None = None,
) -> Callable:
    """Decorator to instrument functions with OpenTelemetry tracing.

    This decorator follows the pattern from grassroots tracer.py.
    Creates a span for the decorated function and automatically
    captures exceptions, function metadata, and custom attributes.

    Args:
        _func: The function to instrument (automatically assigned when used without parentheses)
        span_name: Custom span name (defaults to module.function)
        record_exception: Whether to record exceptions automatically
        attributes: Custom attributes to add to the span
        existing_tracer: Use a specific tracer instead of global

    Returns:
        Callable: Decorated function

    Example:
        ```python
        # Without parentheses (uses defaults)
        @instrument
        async def get_user(user_id: str) -> User:
            pass

        # With parameters
        @instrument(span_name="database.get_user", attributes={"db": "postgres"})
        async def get_user(user_id: str) -> User:
            pass
        ```
    """

    def decorator(func: Callable) -> Callable:
        # Determine span name
        name = span_name or f"{func.__module__}.{func.__qualname__}"

        # Get tracer
        tracer = existing_tracer or get_tracer()

        # Check if function is async
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                with tracer.start_as_current_span(name, record_exception=record_exception) as span:
                    _set_span_attributes(span, func, attributes)
                    try:
                        result = await func(*args, **kwargs)
                    except Exception as e:
                        _set_error_attributes(span, e)
                        raise
                    else:
                        span.set_attribute("operation.success", True)
                        return result

            return async_wrapper

        else:

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                with tracer.start_as_current_span(name, record_exception=record_exception) as span:
                    _set_span_attributes(span, func, attributes)
                    try:
                        result = func(*args, **kwargs)
                    except Exception as e:
                        _set_error_attributes(span, e)
                        raise
                    else:
                        span.set_attribute("operation.success", True)
                        return result

            return sync_wrapper

    # Support both @instrument and @instrument(...)
    if _func is None:
        return decorator
    return decorator(_func)


@contextmanager
def create_span(
    name: str,
    attributes: dict[str, Any] | None = None,
):
    """Context manager to create a nested span.

    Useful for creating spans within instrumented functions for specific operations.

    Args:
        name: Span name
        attributes: Custom attributes to add to the span

    Yields:
        Span: OpenTelemetry span

    Example:
        ```python
        @instrument(span_name="service.process_order")
        async def process_order(order_id: str):
            with create_span("validate_order", {"order_id": order_id}):
                # Validation logic
                pass

            with create_span("charge_payment", {"order_id": order_id}):
                # Payment logic
                pass
        ```
    """
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span(name) as span:
        # Set custom attributes
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, value)

        try:
            yield span
            span.set_status(Status(StatusCode.OK))
            span.set_attribute("operation.success", True)

        except Exception as e:
            # Record exception
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.set_attribute("operation.success", False)
            span.set_attribute("error.type", type(e).__name__)
            span.set_attribute("error.message", str(e))

            # Capture custom error attributes if available
            if hasattr(e, "error_code"):
                span.set_attribute("error.code", e.error_code)

            raise


def add_span_attributes(**attributes: Any) -> None:
    """Add attributes to the current span.

    Args:
        **attributes: Key-value pairs to add as span attributes

    Example:
        ```python
        @instrument(span_name="service.process_user")
        async def process_user(user_id: str):
            user = await get_user(user_id)
            add_span_attributes(
                user_id=user_id,
                user_email=user.email,
                user_role=user.role
            )
        ```
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        for key, value in attributes.items():
            span.set_attribute(key, value)


def add_span_event(name: str, attributes: dict[str, Any] | None = None) -> None:
    """Add an event to the current span.

    Events are timestamped annotations within a span.

    Args:
        name: Event name
        attributes: Event attributes

    Example:
        ```python
        add_span_event("cache_miss", {"key": cache_key})
        add_span_event("retry_attempt", {"attempt": 2, "reason": "timeout"})
        ```
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        span.add_event(name, attributes=attributes or {})


def _set_span_attributes(span: Any, func: Callable, attributes: dict[str, str] | None) -> None:
    """Set all span attributes including semantic, and custom.

    Args:
        span: OpenTelemetry span
        func: Function being traced
        attributes: Custom attributes dictionary
    """
    # OpenTelemetry semantic conventions
    span.set_attribute(SpanAttributes.CODE_NAMESPACE, func.__module__)
    span.set_attribute(SpanAttributes.CODE_FUNCTION, func.__qualname__)
    span.set_attribute(SpanAttributes.CODE_FILEPATH, func.__code__.co_filename)
    span.set_attribute(SpanAttributes.CODE_LINENO, func.__code__.co_firstlineno)

    # Custom attributes
    if attributes:
        for key, value in attributes.items():
            span.set_attribute(key, value)


def _set_error_attributes(span: Any, exception: Exception) -> None:
    """Set error-related attributes on span.

    Args:
        span: OpenTelemetry span
        exception: Exception that occurred
    """
    span.set_attribute("operation.success", False)
    span.set_attribute("error.type", type(exception).__name__)
    span.set_attribute("error.message", str(exception))

    # Capture custom error attributes from application exceptions
    if hasattr(exception, "error_code"):
        span.set_attribute("error.code", exception.error_code)
    if hasattr(exception, "log_detail"):
        span.set_attribute("error.log_detail", exception.log_detail)
