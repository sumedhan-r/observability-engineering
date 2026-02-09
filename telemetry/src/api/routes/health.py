"""Health check routes.

This module provides health check endpoints for the application.
"""

from fastapi import APIRouter

from src.api.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Welcome to Telemetry Sample Application",
        "docs": "/docs",
        "demo_endpoints": "/demo/*",
    }


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    This endpoint is typically excluded from tracing to reduce noise.
    """
    return {"status": "healthy"}
