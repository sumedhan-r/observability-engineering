# Telemetry

Sample FastAPI project demonstrating OpenTelemetry implementation with cloud-agnostic exporter support.

## Features

- Cloud-agnostic design (Azure, AWS, GCP, self-hosted)
- Multiple simultaneous exporters
- `@instrument` decorator for automatic tracing
- Structured logging with OpenTelemetry context
- Flexible sampling strategies
- Clean architecture patterns

## Quick Start

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Configure src/config/settings.yaml
# Set AZURE_MONITOR_CONNECTION_STRING if needed

# Run
uvicorn src.api.main:app --reload
```

Visit http://localhost:8000/docs for API documentation.

## Architecture

**Infrastructure folders** (not feature-based):
- `core/` - Configuration, logging, middleware, lifecycle
- `decorators/` - Cross-cutting concerns (`@instrument`)
- `policies/` - Sampling strategies and business rules
- `dispatchers/` - Multi-exporter telemetry publisher
- `interfaces/` - Abstract base classes
- `connectors/` - Azure Monitor, OTLP, Console exporters
- `routes/` - API endpoints

**Design patterns**: Factory, Observer, Strategy, Decorator, Adapter

## Infrastructure Naming Reference

**Current folders**:
- `decorators/` - Add behavior to functions (`@instrument`, `@cache`, `@retry`)
- `policies/` - Configurable rules (sampling, rate limiting, retention)
- `dispatchers/` - Distribute to multiple destinations (multi-exporter, event publisher)
- `interfaces/` - Abstract contracts (TelemetryExporter, SamplingStrategy)
- `connectors/` - External system adapters (Azure, OTLP, Console)
- `core/` - Foundation components (config, logging, middleware)

**Additional patterns** (as needed):
- `handlers/` - Process events (webhooks, messages, exceptions)
- `interceptors/` - Modify before/after execution (request/response, auth)
- `orchestrators/` - Coordinate workflows (sagas, multi-step processes)
- `resolvers/` - Dynamic configuration (environment-based, feature flags)
- `validators/` - Complex validation logic
- `transformers/` - Data format conversion
- `repositories/` - Data access abstraction
- `guards/` - Access protection (auth, rate limits, circuit breakers)

## Configuration Examples

Edit `src/config/settings.yaml`:

```yaml
# Console (local dev)
- provider: "console"
  enabled: true

# Azure Monitor
- provider: "azure_monitor"
  enabled: true
  azure_monitor:
    connection_string: "${AZURE_MONITOR_CONNECTION_STRING}"

# OTLP (AWS/GCP/Jaeger)
- provider: "otlp"
  enabled: true
  otlp:
    endpoint: "http://localhost:4317"

# Sampling
telemetry:
  sampling_ratio: 0.1
  exclude_endpoints: ["/health", "/metrics"]
```
