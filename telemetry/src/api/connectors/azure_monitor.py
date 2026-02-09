"""Azure Monitor telemetry exporter.

This module implements the TelemetryExporter interface for Azure Monitor.
"""

import structlog
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from src.api.core.config import AzureMonitorConfig
from src.api.interfaces.telemetry_exporter import TelemetryExporter

logger = structlog.get_logger(__name__)


class AzureMonitorExporter(TelemetryExporter):
    """Azure Monitor exporter implementation.

    Sends telemetry data to Azure Application Insights.
    """

    def __init__(self, config: AzureMonitorConfig):
        """Initialize Azure Monitor exporter.

        Args:
            config: Azure Monitor configuration
        """
        self.config = config
        self._exporter: AzureMonitorTraceExporter | None = None
        self._span_processor: BatchSpanProcessor | None = None
        self._connected = False

    async def connect(self) -> None:
        """Establish connection to Azure Monitor."""
        try:
            # Create Azure Monitor trace exporter
            self._exporter = AzureMonitorTraceExporter(connection_string=self.config.connection_string)

            # Create batch span processor
            self._span_processor = BatchSpanProcessor(self._exporter)

            # Configure Azure Monitor with live metrics if enabled
            if self.config.enable_live_metrics:
                configure_azure_monitor(
                    connection_string=self.config.connection_string,
                    enable_live_metrics=True,
                )

            self._connected = True
            logger.info(
                "Connected to Azure Monitor",
                enable_live_metrics=self.config.enable_live_metrics,
            )

        except Exception as e:
            logger.error("Failed to connect to Azure Monitor", error=str(e))
            raise ConnectionError(f"Azure Monitor connection failed: {e}") from e

    async def disconnect(self) -> None:
        """Close connection to Azure Monitor."""
        if self._span_processor:
            # Force flush to ensure all pending spans are exported
            self._span_processor.force_flush()
            self._span_processor.shutdown()
            self._span_processor = None

        self._exporter = None
        self._connected = False
        logger.info("Disconnected from Azure Monitor")

    async def health_check(self) -> bool:
        """Check if Azure Monitor exporter is healthy.

        Returns:
            bool: True if connected, False otherwise
        """
        return self._connected and self._span_processor is not None

    def get_span_processor(self) -> BatchSpanProcessor:
        """Get the span processor for this exporter.

        Returns:
            BatchSpanProcessor: Batch span processor for Azure Monitor

        Raises:
            RuntimeError: If not connected
        """
        if not self._span_processor:
            raise RuntimeError("Azure Monitor exporter not connected. Call connect() first.")
        return self._span_processor

    def get_exporter_info(self) -> dict:
        """Get information about this exporter.

        Returns:
            dict: Exporter metadata
        """
        return {
            "name": "Azure Monitor",
            "type": "azure_monitor",
            "connected": self._connected,
            "enable_live_metrics": self.config.enable_live_metrics,
        }
