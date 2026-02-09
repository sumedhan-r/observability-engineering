"""Sampling strategy interface.

This module defines the Strategy pattern for telemetry sampling decisions.
Different strategies can be implemented for different sampling behaviors.
"""

from abc import ABC, abstractmethod
from typing import Any

from opentelemetry.sdk.trace.sampling import SamplingResult
from opentelemetry.trace import SpanKind
from opentelemetry.util.types import Attributes


class SamplingStrategy(ABC):
    """Abstract base class for sampling strategies.

    Implementations can define different sampling behaviors:
    - AlwaysSample: Sample all spans
    - RatioBasedSampling: Sample X% of spans
    - EndpointExclusionSampling: Exclude specific endpoints
    - AdaptiveSampling: Dynamic sampling based on load
    """

    @abstractmethod
    def should_sample(
        self,
        parent_context: Any,
        trace_id: int,
        name: str,
        kind: SpanKind | None = None,
        attributes: Attributes = None,
        links: Any = None,
        trace_state: Any = None,
    ) -> SamplingResult:
        """Determine if a span should be sampled.

        Args:
            parent_context: Parent span context
            trace_id: Trace ID
            name: Span name
            kind: Span kind (CLIENT, SERVER, etc.)
            attributes: Span attributes
            links: Span links
            trace_state: Trace state

        Returns:
            SamplingResult: Decision to sample or drop the span
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get a human-readable description of this sampling strategy.

        Returns:
            str: Description of the strategy
        """
        pass
