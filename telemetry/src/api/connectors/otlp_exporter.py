"""OTLP telemetry exporter.

This module implements the TelemetryExporter interface for OTLP (OpenTelemetry Protocol).
OTLP is a universal standard that works with any OpenTelemetry-compatible backend.
"""

import structlog
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from src.api.core.config import OTLPConfig
from src.api.interfaces.telemetry_exporter import TelemetryExporter

logger = structlog.get_logger(__name__)


class OTLPExporter(TelemetryExporter):
    """OTLP exporter implementation.

    Sends telemetry data via OpenTelemetry Protocol (OTLP).
    Compatible with:
    - AWS CloudWatch (via OTLP collector)
    - Google Cloud Trace
    - Jaeger
    - Zipkin
    - Any OTLP-compatible backend
    """

    def __init__(self, config: OTLPConfig):
        """Initialize OTLP exporter.

        Args:
            config: OTLP configuration
        """
        self.config = config
        self._exporter: OTLPSpanExporter | None = None
        self._span_processor: BatchSpanProcessor | None = None
        self._connected = False

    async def connect(self) -> None:
        """Establish connection to OTLP endpoint."""
        try:
            # Create OTLP span exporter
            self._exporter = OTLPSpanExporter(
                endpoint=self.config.endpoint,
                headers=self.config.headers,
                insecure=self.config.insecure,
            )

            # Create batch span processor
            self._span_processor = BatchSpanProcessor(self._exporter)

            self._connected = True
            logger.info(
                "Connected to OTLP endpoint",
                endpoint=self.config.endpoint,
                insecure=self.config.insecure,
            )

        except Exception as e:
            logger.error("Failed to connect to OTLP endpoint", error=str(e))
            raise ConnectionError(f"OTLP connection failed: {e}") from e

    async def disconnect(self) -> None:
        """Close connection to OTLP endpoint."""
        if self._span_processor:
            # Force flush to ensure all pending spans are exported
            self._span_processor.force_flush()
            self._span_processor.shutdown()
            self._span_processor = None

        self._exporter = None
        self._connected = False
        logger.info("Disconnected from OTLP endpoint")

    async def health_check(self) -> bool:
        """Check if OTLP exporter is healthy.

        Returns:
            bool: True if connected, False otherwise
        """
        return self._connected and self._span_processor is not None

    def get_span_processor(self) -> BatchSpanProcessor:
        """Get the span processor for this exporter.

        Returns:
            BatchSpanProcessor: Batch span processor for OTLP

        Raises:
            RuntimeError: If not connected
        """
        if not self._span_processor:
            raise RuntimeError("OTLP exporter not connected. Call connect() first.")
        return self._span_processor

    def get_exporter_info(self) -> dict:
        """Get information about this exporter.

        Returns:
            dict: Exporter metadata
        """
        return {
            "name": "OTLP",
            "type": "otlp",
            "connected": self._connected,
            "endpoint": self.config.endpoint,
            "insecure": self.config.insecure,
        }
