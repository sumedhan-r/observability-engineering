"""Application lifespan management.

This module manages application startup and shutdown events.
Follows the pattern from workforce project.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.api.core.logger import get_logger
from src.api.dispatchers.telemetry import cleanup_telemetry, initialize_telemetry
from src.config.loader import load_config

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifespan events.

    Handles startup and shutdown operations for the FastAPI application.
    This replaces the deprecated @app.on_event decorators.

    Args:
        app: FastAPI application instance

    Yields:
        None: Control back to the application during its runtime
    """
    # Startup
    logger.info("Starting Telemetry Sample Application")

    try:
        # Load configuration and initialize telemetry
        config = load_config()
        await initialize_telemetry(config, app)
        logger.info("Application startup complete")

    except Exception as e:
        logger.error("Failed to start application", error=str(e))
        raise

    yield  # Application runs here

    # Shutdown
    logger.info("Shutting down application...")

    try:
        # Cleanup telemetry
        await cleanup_telemetry()
        logger.info("Telemetry system cleaned up successfully")

    except Exception as e:
        logger.error("Error during telemetry cleanup", error=str(e))

    logger.info("Application shutdown complete")
