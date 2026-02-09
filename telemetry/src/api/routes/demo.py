"""Demo routes to showcase telemetry instrumentation.

This module demonstrates how to use the telemetry system in practice.
"""

import random
import time
from typing import Any

from fastapi import APIRouter, HTTPException

from src.api.decorators.instrumentation import (
    add_span_attributes,
    add_span_event,
    create_span,
    instrument,
)
from src.api.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/simple")
@instrument(span_name="demo.simple_operation")
async def simple_operation() -> dict[str, str]:
    """Simple operation with automatic instrumentation."""
    logger.info("Executing simple operation")
    return {"message": "This operation is automatically traced!"}


@router.get("/with-attributes")
@instrument(
    span_name="demo.operation_with_attributes",
    attributes={"operation_type": "demo", "version": "1.0"},
)
async def operation_with_attributes(user_id: str = "anonymous") -> dict[str, Any]:
    """Operation with custom span attributes."""
    # Add dynamic attributes to current span
    add_span_attributes(
        user_id=user_id,
        processing_stage="initial",
    )

    logger.info("Processing request", user_id=user_id)

    # Simulate some work
    time.sleep(0.1)

    # Update span attribute
    add_span_attributes(processing_stage="completed")

    attributes_added: Any = ["user_id", "processing_stage", "operation_type"]

    return {
        "message": "Operation completed",
        "user_id": user_id,
        "attributes_added": attributes_added,
    }


@router.get("/nested-spans")
@instrument(span_name="demo.operation_with_nested_spans")
async def operation_with_nested_spans() -> dict[str, Any]:
    """Operation with nested spans for fine-grained tracing."""
    logger.info("Starting operation with nested spans")

    results: dict[str, Any] = {}

    # First nested operation
    with create_span("validate_input", {"validation_type": "schema"}):
        add_span_event("validation_started")
        time.sleep(0.05)
        results["validation"] = "passed"
        add_span_event("validation_completed", {"result": "passed"})

    # Second nested operation
    with create_span("fetch_data", {"data_source": "database"}):
        add_span_event("database_query_started")
        time.sleep(0.1)
        results["data"] = {"id": 123, "name": "Sample"}
        add_span_event("database_query_completed", {"rows": 1})

    # Third nested operation
    with create_span("process_data", {"processor": "v2"}):
        add_span_event("processing_started")
        time.sleep(0.05)
        results["processed"] = True
        add_span_event("processing_completed")

    span_hierarchy: Any = "parent -> validate_input, fetch_data, process_data"

    return {
        "message": "Operation with nested spans completed",
        "results": results,
        "span_hierarchy": span_hierarchy,
    }


@router.get("/error-handling")
@instrument(span_name="demo.operation_with_error")
async def operation_with_error(should_fail: bool = False) -> dict[str, Any]:
    """Operation demonstrating error handling in spans."""
    add_span_attributes(should_fail=should_fail)

    if should_fail:
        # This error will be automatically captured in the span
        logger.error("Operation intentionally failed")
        raise HTTPException(status_code=500, detail="Intentional error for demonstration")

    return {"message": "Operation succeeded", "error": "none"}


@router.get("/slow-operation")
@instrument(span_name="demo.slow_operation")
async def slow_operation(duration_ms: int = 500) -> dict[str, Any]:
    """Slow operation to demonstrate performance tracking."""
    add_span_attributes(requested_duration_ms=duration_ms)
    add_span_event("operation_started")

    # Simulate slow operation
    time.sleep(duration_ms / 1000)

    add_span_event("operation_completed")

    note: Any = "Check trace to see span duration"

    return {
        "message": "Slow operation completed",
        "duration_ms": duration_ms,
        "note": note,
    }


@router.get("/complex-workflow")
@instrument(span_name="demo.complex_workflow")
async def complex_workflow(user_id: str = "user123") -> dict[str, Any]:
    """Complex workflow demonstrating multiple telemetry features."""
    add_span_attributes(
        user_id=user_id,
        workflow_version="2.0",
        environment="demo",
    )

    results: dict[str, Any] = {}

    # Step 1: Authentication
    with create_span("authenticate_user", {"user_id": user_id}):
        add_span_event("auth_started")
        time.sleep(0.05)
        is_authenticated = True
        add_span_attributes(authenticated=is_authenticated)
        add_span_event("auth_completed", {"success": True})
        results["auth"] = "success"

    # Step 2: Fetch user data
    with create_span("fetch_user_data", {"user_id": user_id}):
        add_span_event("database_query_started", {"table": "users"})
        time.sleep(0.1)
        user_data = {"id": user_id, "name": "Demo User", "role": "admin"}
        add_span_attributes(user_role=user_data["role"])
        add_span_event("database_query_completed", {"rows_returned": 1})
        results["user_data"] = user_data

    # Step 3: Check permissions
    with create_span("check_permissions", {"user_role": user_data["role"]}):
        add_span_event("permission_check_started")
        time.sleep(0.05)
        has_permission = user_data["role"] == "admin"
        add_span_attributes(has_permission=has_permission)
        add_span_event("permission_check_completed", {"result": has_permission})
        results["permissions"] = "granted" if has_permission else "denied"

    # Step 4: Process business logic
    with create_span("process_business_logic", {"operation": "complex_calculation"}):
        add_span_event("calculation_started")

        # Simulate some complexity
        for i in range(3):
            add_span_event(f"calculation_step_{i + 1}", {"step": i + 1})
            time.sleep(0.03)

        calculation_result = random.randint(100, 999)
        add_span_attributes(calculation_result=calculation_result)
        add_span_event("calculation_completed", {"result": calculation_result})
        results["calculation"] = calculation_result

    # Step 5: Save results
    with create_span("save_results", {"destination": "database"}):
        add_span_event("save_started")
        time.sleep(0.05)
        add_span_event("save_completed", {"records_saved": 1})
        results["saved"] = True

    telemetry_features: Any = [
        "Custom span attributes",
        "Nested spans",
        "Span events",
        "Dynamic attributes",
        "Error tracking",
    ]

    return {
        "message": "Complex workflow completed successfully",
        "results": results,
        "telemetry_features": telemetry_features,
    }
