"""Telemetry exporter interface.

This module defines the abstract base class for all telemetry exporters.
Following the Interface pattern from the workforce project architecture.
"""

from abc import ABC, abstractmethod
from typing import Any


class TelemetryExporter(ABC):
    """Abstract base class for telemetry exporters.

    All concrete exporters (Azure Monitor, OTLP, Console, Jaeger, etc.)
    must implement this interface.
    """

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the telemetry backend.

        This method should handle any initialization logic such as:
        - Creating client connections
        - Validating credentials
        - Testing connectivity

        Raises:
            ConnectionError: If connection fails
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to the telemetry backend.

        This method should handle cleanup such as:
        - Flushing pending data
        - Closing client connections
        - Releasing resources
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the exporter is healthy and operational.

        Returns:
            bool: True if healthy, False otherwise
        """
        pass

    @abstractmethod
    def get_span_processor(self) -> Any:
        """Get the OpenTelemetry span processor for this exporter.

        Returns:
            SpanProcessor: An OpenTelemetry span processor instance
        """
        pass

    @abstractmethod
    def get_exporter_info(self) -> dict[str, Any]:
        """Get information about this exporter.

        Returns:
            dict: Exporter metadata (name, type, config, etc.)
        """
        pass
