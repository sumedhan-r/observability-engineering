"""Console telemetry exporter.

This module implements the TelemetryExporter interface for console output.
Useful for local development and debugging.
"""

import structlog
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from src.api.core.config import ConsoleConfig
from src.api.interfaces.telemetry_exporter import TelemetryExporter

logger = structlog.get_logger(__name__)


class ConsoleExporter(TelemetryExporter):
    """Console exporter implementation.

    Outputs telemetry data to console (stdout).
    Useful for local development and debugging.
    """

    def __init__(self, config: ConsoleConfig):
        """Initialize console exporter.

        Args:
            config: Console exporter configuration
        """
        self.config = config
        self._exporter: ConsoleSpanExporter | None = None
        self._span_processor: BatchSpanProcessor | None = None
        self._connected = False

    async def connect(self) -> None:
        """Initialize console exporter."""
        try:
            # Create console span exporter
            self._exporter = ConsoleSpanExporter()

            # Create batch span processor
            self._span_processor = BatchSpanProcessor(self._exporter)

            self._connected = True
            logger.info(
                "Console exporter initialized",
                pretty_print=self.config.pretty_print,
            )

        except Exception as e:
            logger.error("Failed to initialize console exporter", error=str(e))
            raise ConnectionError(f"Console exporter initialization failed: {e}") from e

    async def disconnect(self) -> None:
        """Shutdown console exporter."""
        if self._span_processor:
            # Force flush to ensure all pending spans are exported
            self._span_processor.force_flush()
            self._span_processor.shutdown()
            self._span_processor = None

        self._exporter = None
        self._connected = False
        logger.info("Console exporter shut down")

    async def health_check(self) -> bool:
        """Check if console exporter is healthy.

        Returns:
            bool: True if initialized, False otherwise
        """
        return self._connected and self._span_processor is not None

    def get_span_processor(self) -> BatchSpanProcessor:
        """Get the span processor for this exporter.

        Returns:
            BatchSpanProcessor: Batch span processor for console output

        Raises:
            RuntimeError: If not connected
        """
        if not self._span_processor:
            raise RuntimeError("Console exporter not initialized. Call connect() first.")
        return self._span_processor

    def get_exporter_info(self) -> dict:
        """Get information about this exporter.

        Returns:
            dict: Exporter metadata
        """
        return {
            "name": "Console",
            "type": "console",
            "connected": self._connected,
            "pretty_print": self.config.pretty_print,
        }
