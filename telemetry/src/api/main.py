"""Main FastAPI application entry point.

Follows the pattern from workforce project main.py.
"""

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from src.api.core.lifespan import lifespan
from src.api.core.logger import get_logger
from src.api.core.middleware import StructuredLoggingMiddleware
from src.api.routes.api import api_router
from src.config.loader import load_config

# Load configuration
config = load_config()

# Get logger
logger = get_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Telemetry Sample Application",
    description="Sample application demonstrating hybrid telemetry design patterns",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Instrument FastAPI with OpenTelemetry
# This enables automatic tracing of all HTTP requests
FastAPIInstrumentor.instrument_app(app)
logger.info("FastAPI instrumented for automatic tracing")

# Observability middleware
app.add_middleware(StructuredLoggingMiddleware)
app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Correlation-ID",
    update_request_header=True,
)
logger.info("Observability middleware enabled")

# Include API router (aggregates all routes)
app.include_router(api_router)


# For local development
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
