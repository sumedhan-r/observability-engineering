"""API router aggregator.

This module aggregates all API routes into a single parent router.
Follows the pattern from workforce project.
"""

from fastapi import APIRouter

from src.api.routes import demo, health

# Create parent router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(
    health.router,
    tags=["health"],
)

api_router.include_router(
    demo.router,
    prefix="/demo",
    tags=["demo"],
)
