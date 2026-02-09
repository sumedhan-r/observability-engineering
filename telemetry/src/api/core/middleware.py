"""Simple observability middleware for FastAPI applications.

This module provides basic middleware for structured logging with correlation IDs.
Follows a simplified pattern from the workforce project.
"""

import time
from collections.abc import Awaitable, Callable

from asgi_correlation_id import correlation_id
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from src.api.core.logger import bind_context, clear_context, get_logger


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to add structured logging context to requests.

    Logs:
    - Request start with method, path, correlation_id
    - Request completion with status_code, process_time_ms
    - Request failures with error details

    Binds context variables:
    - correlation_id (from CorrelationIdMiddleware)
    - method (HTTP method)
    - path (request path)
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.logger = get_logger(__name__)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        # Get correlation ID from asgi-correlation-id middleware
        # CorrelationIdMiddleware must run before this
        corr_id: str = correlation_id.get() or "unknown"

        # Clear any existing context from previous request
        clear_context()

        # Bind request context for all logs during this request
        bind_context(
            correlation_id=corr_id,
            method=request.method,
            path=request.url.path,
        )

        start_time = time.time()

        # Log request start
        self.logger.info(
            "Request started",
            method=request.method,
            path=request.url.path,
            correlation_id=corr_id,
        )

        try:
            # Process request
            response = await call_next(request)

        except Exception as e:
            # Log request error
            process_time = time.time() - start_time

            # Build error context
            error_context = {
                "error": str(e),
                "error_type": type(e).__name__,
                "process_time_ms": round(process_time * 1000, 2),
                "correlation_id": corr_id,
            }

            # Add custom error fields if present
            if hasattr(e, "error_code"):
                error_context["error_code"] = e.error_code
            if hasattr(e, "log_detail"):
                error_context["log_detail"] = e.log_detail

            self.logger.exception("Request failed", **error_context)
            raise

        else:
            # Calculate processing time
            process_time = time.time() - start_time

            # Log request completion
            self.logger.info(
                "Request completed",
                status_code=response.status_code,
                process_time_ms=round(process_time * 1000, 2),
                correlation_id=corr_id,
            )

            return response

        finally:
            # Clear context after request
            clear_context()
