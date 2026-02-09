"""Configuration loader for YAML settings.

This module handles loading configuration from YAML files.
"""

import os
from pathlib import Path

import yaml

from src.api.core.config import TelemetryConfig


def load_config(config_path: str | Path | None = None) -> TelemetryConfig:
    """Load telemetry configuration from YAML file.

    Args:
        config_path: Path to configuration file. If None, uses default path.

    Returns:
        TelemetryConfig: Loaded and validated configuration

    Raises:
        FileNotFoundError: If configuration file not found
        ValueError: If configuration is invalid
    """
    config_path_obj: Path
    if config_path is None:
        # Default to settings.yaml in config directory
        config_dir = Path(__file__).parent
        config_path_obj = config_dir / "settings.yaml"
    else:
        config_path_obj = Path(config_path)

    if not config_path_obj.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path_obj}")

    # Load YAML
    with open(config_path_obj) as f:
        config_data = yaml.safe_load(f)

    # Extract telemetry configuration
    telemetry_config = config_data.get("telemetry")
    if not telemetry_config:
        raise ValueError("Missing 'telemetry' section in configuration file")

    # Override with environment variables if present
    telemetry_config = _apply_env_overrides(telemetry_config)

    # Validate and create TelemetryConfig
    return TelemetryConfig(**telemetry_config)


def _apply_env_overrides(config: dict) -> dict:
    """Apply environment variable overrides to configuration.

    Environment variables follow the pattern:
    TELEMETRY_SERVICE_NAME, TELEMETRY_SERVICE_VERSION, etc.

    Args:
        config: Configuration dictionary

    Returns:
        dict: Configuration with environment overrides applied
    """
    # Service-level overrides
    if env_service_name := os.getenv("TELEMETRY_SERVICE_NAME"):
        config["service_name"] = env_service_name

    if env_service_version := os.getenv("TELEMETRY_SERVICE_VERSION"):
        config["service_version"] = env_service_version

    if env_environment := os.getenv("TELEMETRY_ENVIRONMENT"):
        config["environment"] = env_environment

    # Exporter-level overrides
    # Example: AZURE_MONITOR_CONNECTION_STRING
    for exporter_config in config.get("exporters", []):
        provider = exporter_config.get("provider")

        if provider == "azure_monitor":
            if connection_string := os.getenv("AZURE_MONITOR_CONNECTION_STRING"):
                if "azure_monitor" not in exporter_config:
                    exporter_config["azure_monitor"] = {}
                exporter_config["azure_monitor"]["connection_string"] = connection_string

        elif provider == "otlp":
            if endpoint := os.getenv("OTLP_ENDPOINT"):
                if "otlp" not in exporter_config:
                    exporter_config["otlp"] = {}
                exporter_config["otlp"]["endpoint"] = endpoint

    return config
