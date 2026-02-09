"""Telemetry system setup and management.

This module contains:
- TelemetryPublisher (Observer pattern for multiple exporters)
- Factory functions for creating exporters
- Initialization and cleanup functions
- Global telemetry management

Merged from: telemetry_publisher.py, dependencies.py, tracer.py
"""

from typing import Any

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.semconv.resource import ResourceAttributes

from src.api.connectors.azure_monitor import AzureMonitorExporter
from src.api.connectors.console_exporter import ConsoleExporter
from src.api.connectors.otlp_exporter import OTLPExporter
from src.api.core.config import ExporterConfig, TelemetryConfig
from src.api.decorators.instrumentation import set_global_tracer
from src.api.core.logger import get_logger
from src.api.interfaces.telemetry_exporter import TelemetryExporter

logger = get_logger(__name__)

# Exporter Registry - Maps provider name to exporter class (Factory pattern)
TELEMETRY_EXPORTERS = {
    "azure_monitor": AzureMonitorExporter,
    "otlp": OTLPExporter,
    "console": ConsoleExporter,
    # Future exporters can be added here:
    # "jaeger": JaegerExporter,
    # "zipkin": ZipkinExporter,
    # "datadog": DatadogExporter,
}

# Global singleton instance
_telemetry_publisher: "TelemetryPublisher | None" = None


# ==============================================================================
# TelemetryPublisher (Observer Pattern)
# ==============================================================================


class TelemetryPublisher:
    """Telemetry publisher implementing the Observer pattern.

    Manages multiple telemetry exporters and coordinates span processing.
    Allows sending telemetry to multiple backends simultaneously
    (e.g., Azure Monitor + Console for debugging).
    """

    def __init__(self, config: TelemetryConfig):
        """Initialize telemetry publisher.

        Args:
            config: Telemetry configuration
        """
        self.config = config
        self._exporters: list[TelemetryExporter] = []
        self._tracer_provider: TracerProvider | None = None
        self._initialized = False

    def attach(self, exporter: TelemetryExporter) -> None:
        """Attach an exporter to the publisher.

        Args:
            exporter: Telemetry exporter to attach
        """
        if exporter not in self._exporters:
            self._exporters.append(exporter)
            logger.info(
                "Exporter attached to publisher",
                exporter_info=exporter.get_exporter_info(),
            )

    def detach(self, exporter: TelemetryExporter) -> None:
        """Detach an exporter from the publisher.

        Args:
            exporter: Telemetry exporter to detach
        """
        if exporter in self._exporters:
            self._exporters.remove(exporter)
            logger.info(
                "Exporter detached from publisher",
                exporter_info=exporter.get_exporter_info(),
            )

    async def initialize(self) -> None:
        """Initialize the telemetry publisher.

        Creates the tracer provider and configures all attached exporters.
        """
        if self._initialized:
            logger.warning("Telemetry publisher already initialized")
            return

        try:
            # Create service resource with metadata
            resource = self._create_service_resource()

            # Create tracer provider
            self._tracer_provider = TracerProvider(resource=resource)

            # Add span processors from all exporters
            for exporter in self._exporters:
                span_processor = exporter.get_span_processor()
                self._tracer_provider.add_span_processor(span_processor)
                logger.info(
                    "Added span processor",
                    exporter_info=exporter.get_exporter_info(),
                )

            # Set global tracer provider
            trace.set_tracer_provider(self._tracer_provider)

            self._initialized = True
            logger.info(
                "Telemetry publisher initialized",
                service_name=self.config.service_name,
                service_version=self.config.service_version,
                exporter_count=len(self._exporters),
            )

        except Exception as e:
            logger.error("Failed to initialize telemetry publisher", error=str(e))
            raise

    async def shutdown(self) -> None:
        """Shutdown the telemetry publisher.

        Flushes all pending spans and shuts down tracer provider.
        """
        if not self._initialized:
            return

        try:
            # Shutdown tracer provider (flushes all span processors)
            if self._tracer_provider:
                self._tracer_provider.shutdown()

            self._initialized = False
            logger.info("Telemetry publisher shut down")

        except Exception as e:
            logger.error("Error during telemetry publisher shutdown", error=str(e))
            raise

    def get_tracer(self, name: str) -> trace.Tracer:
        """Get a tracer instance.

        Args:
            name: Name of the tracer (usually __name__)

        Returns:
            Tracer: OpenTelemetry tracer instance

        Raises:
            RuntimeError: If publisher not initialized
        """
        if not self._initialized or not self._tracer_provider:
            raise RuntimeError("Telemetry publisher not initialized. Call initialize() first.")
        return trace.get_tracer(name, tracer_provider=self._tracer_provider)

    async def health_check(self) -> dict[str, Any]:
        """Check health of all exporters.

        Returns:
            dict: Health status of all exporters
        """
        health_status: dict[str, Any] = {
            "initialized": self._initialized,
            "exporters": [],
        }

        for exporter in self._exporters:
            exporter_info = exporter.get_exporter_info()
            exporter_health = await exporter.health_check()
            health_status["exporters"].append(
                {
                    "info": exporter_info,
                    "healthy": exporter_health,
                }
            )

        return health_status

    def _create_service_resource(self) -> Resource:
        """Create OpenTelemetry Resource with service metadata.

        Returns:
            Resource: Service resource with attributes
        """
        attributes = {
            ResourceAttributes.SERVICE_NAME: self.config.service_name,
            ResourceAttributes.SERVICE_VERSION: self.config.service_version,
            ResourceAttributes.DEPLOYMENT_ENVIRONMENT: self.config.environment,
        }

        return Resource(attributes=attributes)

    def get_exporter_count(self) -> int:
        """Get the number of attached exporters.

        Returns:
            int: Number of exporters
        """
        return len(self._exporters)

    def list_exporters(self) -> list[dict]:
        """List all attached exporters.

        Returns:
            list[dict]: List of exporter information
        """
        return [exporter.get_exporter_info() for exporter in self._exporters]


# ==============================================================================
# Factory Functions
# ==============================================================================


def create_exporter(exporter_config: ExporterConfig) -> TelemetryExporter:
    """Factory function to create a telemetry exporter.

    Args:
        exporter_config: Exporter configuration

    Returns:
        TelemetryExporter: Configured exporter instance

    Raises:
        ValueError: If provider is unknown or configuration is invalid
    """
    provider = exporter_config.provider

    # Look up exporter class in registry
    exporter_class = TELEMETRY_EXPORTERS.get(provider)
    if not exporter_class:
        available = ", ".join(TELEMETRY_EXPORTERS.keys())
        raise ValueError(f"Unknown telemetry provider: {provider}. Available providers: {available}")

    # Get provider-specific configuration
    provider_config = exporter_config.get_provider_config()

    # Create exporter instance with typed configuration
    exporter: TelemetryExporter = exporter_class(provider_config)

    logger.info(
        "Created telemetry exporter",
        provider=provider,
        config=provider_config.model_dump(),
    )

    return exporter


# ==============================================================================
# Initialization and Cleanup
# ==============================================================================


async def initialize_telemetry(config: TelemetryConfig, app=None) -> TelemetryPublisher:
    """Initialize telemetry system with all configured exporters.

    This is the main entry point for setting up telemetry.
    It follows these steps:
    1. Create TelemetryPublisher (Observer)
    2. Create all enabled exporters (Factory)
    3. Connect each exporter
    4. Attach exporters to publisher
    5. Initialize publisher with tracer provider
    6. Set global tracer
    7. Instrument FastAPI (if app provided)

    Args:
        config: Telemetry configuration
        app: Optional FastAPI application instance for automatic instrumentation

    Returns:
        TelemetryPublisher: Initialized telemetry publisher

    Raises:
        ValueError: If no exporters are configured
        ConnectionError: If exporter connection fails
    """
    global _telemetry_publisher

    # Create publisher
    publisher = TelemetryPublisher(config)

    # Get enabled exporters
    enabled_exporters = config.get_enabled_exporters()
    if not enabled_exporters:
        raise ValueError("No enabled exporters found in configuration")

    logger.info(
        "Initializing telemetry system",
        service_name=config.service_name,
        service_version=config.service_version,
        environment=config.environment,
        exporter_count=len(enabled_exporters),
    )

    # Create and connect each exporter
    for exporter_config in enabled_exporters:
        try:
            # Create exporter using factory
            exporter = create_exporter(exporter_config)

            # Connect to backend
            await exporter.connect()

            # Attach to publisher (Observer pattern)
            publisher.attach(exporter)

            logger.info(
                "Exporter initialized and attached",
                exporter_info=exporter.get_exporter_info(),
            )

        except Exception as e:
            logger.error(
                "Failed to initialize exporter",
                provider=exporter_config.provider,
                error=str(e),
            )
            # Continue with other exporters instead of failing completely
            continue

    # Initialize publisher (creates tracer provider and registers span processors)
    await publisher.initialize()

    # Get tracer and set as global
    tracer = publisher.get_tracer(__name__)
    set_global_tracer(tracer)

    logger.info(
        "Global tracer set",
        service_name=config.service_name,
    )

    # Instrument FastAPI if app provided
    if app:
        FastAPIInstrumentor.instrument_app(app)
        logger.info("FastAPI instrumented for automatic tracing")

    # Store global reference
    _telemetry_publisher = publisher

    logger.info(
        "Telemetry system initialized successfully",
        exporter_count=publisher.get_exporter_count(),
    )

    return publisher


async def cleanup_telemetry() -> None:
    """Cleanup telemetry system.

    Disconnects all exporters and shuts down the publisher.
    """
    global _telemetry_publisher

    if not _telemetry_publisher:
        logger.warning("No telemetry publisher to cleanup")
        return

    logger.info("Cleaning up telemetry system")

    try:
        # Shutdown publisher (flushes and closes span processors)
        await _telemetry_publisher.shutdown()

        # Disconnect all exporters
        for exporter_info in _telemetry_publisher.list_exporters():
            logger.info("Exporter cleaned up", exporter_info=exporter_info)

        _telemetry_publisher = None
        logger.info("Telemetry system cleaned up successfully")

    except Exception as e:
        logger.error("Error during telemetry cleanup", error=str(e))
        raise


# ==============================================================================
# Getter Functions
# ==============================================================================


def get_telemetry_publisher() -> TelemetryPublisher:
    """Get the global telemetry publisher instance.

    Returns:
        TelemetryPublisher: Global telemetry publisher

    Raises:
        RuntimeError: If telemetry not initialized
    """
    if _telemetry_publisher is None:
        raise RuntimeError("Telemetry not initialized. Call initialize_telemetry() first.")
    return _telemetry_publisher


async def telemetry_health_check() -> dict:
    """Check health of telemetry system.

    Returns:
        dict: Health status of telemetry system
    """
    if _telemetry_publisher is None:
        return {
            "initialized": False,
            "exporters": [],
        }

    return await _telemetry_publisher.health_check()
