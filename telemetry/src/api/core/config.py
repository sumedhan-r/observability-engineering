"""Configuration models for telemetry system.

This module defines Pydantic models for type-safe configuration management.
Following the workforce project's configuration pattern.
"""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class AzureMonitorConfig(BaseModel):
    """Configuration for Azure Monitor exporter."""

    connection_string: str = Field(..., description="Azure Application Insights connection string")
    enable_live_metrics: bool = Field(default=True, description="Enable Azure Monitor live metrics")


class OTLPConfig(BaseModel):
    """Configuration for OTLP exporter."""

    endpoint: str = Field(default="http://localhost:4317", description="OTLP endpoint URL")
    headers: dict[str, str] = Field(default_factory=dict, description="Headers to send with OTLP requests")
    insecure: bool = Field(default=False, description="Use insecure connection (no TLS)")


class ConsoleConfig(BaseModel):
    """Configuration for Console exporter."""

    pretty_print: bool = Field(default=True, description="Pretty print JSON output")


class JaegerConfig(BaseModel):
    """Configuration for Jaeger exporter."""

    agent_host: str = Field(default="localhost", description="Jaeger agent host")
    agent_port: int = Field(default=6831, description="Jaeger agent port")


class ExporterConfig(BaseModel):
    """Configuration for a single exporter instance."""

    provider: Literal["azure_monitor", "otlp", "console", "jaeger"] = Field(
        ..., description="Telemetry exporter provider to use"
    )
    enabled: bool = Field(default=True, description="Enable this exporter")

    # Sampling configuration
    sampling_ratio: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Sampling ratio (0.0 = 0%, 1.0 = 100%)",
    )
    exclude_endpoints: list[str] = Field(
        default_factory=lambda: ["health", "docs", "openapi.json"],
        description="Endpoints to exclude from tracing",
    )

    # Decorator features
    enable_batching: bool = Field(default=True, description="Enable span batching")
    batch_size: int = Field(default=512, ge=1, description="Maximum batch size for spans")
    batch_timeout_ms: int = Field(default=5000, ge=100, description="Maximum time to wait before exporting batch (ms)")

    # Provider-specific configurations
    azure_monitor: AzureMonitorConfig | None = None
    otlp: OTLPConfig | None = None
    console: ConsoleConfig | None = None
    jaeger: JaegerConfig | None = None

    @field_validator("sampling_ratio")
    @classmethod
    def validate_sampling_ratio(cls, v: float) -> float:
        """Validate sampling ratio is between 0.0 and 1.0."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("sampling_ratio must be between 0.0 and 1.0")
        return v

    def get_provider_config(self) -> AzureMonitorConfig | OTLPConfig | ConsoleConfig | JaegerConfig:
        """Get the configuration for the active provider.

        Returns:
            Provider-specific configuration

        Raises:
            ValueError: If provider configuration is missing
        """
        provider_config: AzureMonitorConfig | OTLPConfig | ConsoleConfig | JaegerConfig | None = getattr(
            self, self.provider, None
        )
        if provider_config is None:
            raise ValueError(
                f"Configuration for provider '{self.provider}' is missing. "
                f"Please provide '{self.provider}' configuration section."
            )
        return provider_config


class TelemetryConfig(BaseModel):
    """Root configuration for telemetry system."""

    service_name: str = Field(..., description="Service name for telemetry")
    service_version: str = Field(default="1.0.0", description="Service version")
    environment: str = Field(default="local", description="Deployment environment")

    exporters: list[ExporterConfig] = Field(default_factory=list, description="List of telemetry exporters to enable")

    @field_validator("exporters")
    @classmethod
    def validate_exporters(cls, v: list[ExporterConfig]) -> list[ExporterConfig]:
        """Validate at least one exporter is configured."""
        if not v:
            raise ValueError("At least one exporter must be configured")
        return v

    def get_enabled_exporters(self) -> list[ExporterConfig]:
        """Get list of enabled exporters.

        Returns:
            list[ExporterConfig]: Enabled exporter configurations
        """
        return [e for e in self.exporters if e.enabled]
