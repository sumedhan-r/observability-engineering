"""Sampling strategy implementations.

This module implements the Strategy pattern for different sampling behaviors.
"""

from typing import Sequence

from opentelemetry.context import Context
from opentelemetry.sdk.trace.sampling import (
    Decision,
    ParentBased,
    Sampler,
    SamplingResult,
    TraceIdRatioBased,
)
from opentelemetry.trace import Link, SpanKind, get_current_span
from opentelemetry.trace.span import TraceState
from opentelemetry.util.types import Attributes

from src.api.interfaces.sampling_strategy import SamplingStrategy


class AlwaysSampleStrategy(SamplingStrategy, Sampler):
    """Always sample all spans.

    Useful for development or when you want complete trace visibility.
    """

    def should_sample(
        self,
        parent_context: Context | None,
        trace_id: int,
        name: str,
        kind: SpanKind | None = None,
        attributes: Attributes = None,
        links: Sequence[Link] | None = None,
        trace_state: TraceState | None = None,
    ) -> SamplingResult:
        """Always return RECORD_AND_SAMPLE decision."""
        return SamplingResult(Decision.RECORD_AND_SAMPLE, attributes, trace_state)

    def get_description(self) -> str:
        """Get description of this strategy."""
        return "AlwaysSample: Samples 100% of all spans"


class RatioBasedSamplingStrategy(SamplingStrategy, Sampler):
    """Sample a percentage of spans based on trace ID.

    This is deterministic - the same trace ID will always produce the same decision.
    """

    def __init__(self, ratio: float = 1.0):
        """Initialize ratio-based sampler.

        Args:
            ratio: Sampling ratio between 0.0 and 1.0 (0% to 100%)
        """
        if not 0.0 <= ratio <= 1.0:
            raise ValueError(f"Sampling ratio must be between 0.0 and 1.0, got {ratio}")
        self.ratio = ratio
        self._sampler = TraceIdRatioBased(ratio)

    def should_sample(
        self,
        parent_context: Context | None,
        trace_id: int,
        name: str,
        kind: SpanKind | None = None,
        attributes: Attributes = None,
        links: Sequence[Link] | None = None,
        trace_state: TraceState | None = None,
    ) -> SamplingResult:
        """Sample based on trace ID ratio."""
        return self._sampler.should_sample(parent_context, trace_id, name, kind, attributes, links, trace_state)

    def get_description(self) -> str:
        """Get description of this strategy."""
        return f"RatioBasedSampling: Samples {self.ratio * 100:.1f}% of spans"


class EndpointExclusionSamplingStrategy(SamplingStrategy, Sampler):
    """Exclude specific endpoints from sampling while sampling others.

    Useful for excluding health checks, metrics endpoints, etc.
    """

    def __init__(self, base_sampler: Sampler, exclude_patterns: list[str]):
        """Initialize endpoint exclusion sampler.

        Args:
            base_sampler: Base sampler to use for non-excluded spans
            exclude_patterns: List of string patterns to exclude (substring match)
        """
        self.base_sampler = base_sampler
        self.exclude_patterns = exclude_patterns or []

    def should_sample(
        self,
        parent_context: Context | None,
        trace_id: int,
        name: str,
        kind: SpanKind | None = None,
        attributes: Attributes = None,
        links: Sequence[Link] | None = None,
        trace_state: TraceState | None = None,
    ) -> SamplingResult:
        """Check if span name matches exclusion patterns."""
        # Check if span name contains any exclusion pattern
        if any(pattern in name for pattern in self.exclude_patterns):
            # Preserve parent trace state if available
            if parent_context:
                parent_span_context = get_current_span(parent_context).get_span_context()
                if parent_span_context and parent_span_context.trace_state:
                    trace_state = parent_span_context.trace_state

            return SamplingResult(Decision.DROP, attributes, trace_state)

        # Use base sampler for non-excluded spans
        return self.base_sampler.should_sample(parent_context, trace_id, name, kind, attributes, links, trace_state)

    def get_description(self) -> str:
        """Get description of this strategy."""
        patterns = ", ".join(self.exclude_patterns)
        return f"EndpointExclusionSampling: Excludes patterns [{patterns}]"


class ParentBasedSamplingStrategy(SamplingStrategy, Sampler):
    """Respect parent span sampling decision.

    If parent span is sampled, child spans are sampled.
    If parent span is not sampled, child spans are not sampled.
    If no parent, use base sampler.
    """

    def __init__(self, base_sampler: Sampler):
        """Initialize parent-based sampler.

        Args:
            base_sampler: Sampler to use when there's no parent span
        """
        self.base_sampler = base_sampler
        self._sampler = ParentBased(base_sampler)

    def should_sample(
        self,
        parent_context: Context | None,
        trace_id: int,
        name: str,
        kind: SpanKind | None = None,
        attributes: Attributes = None,
        links: Sequence[Link] | None = None,
        trace_state: TraceState | None = None,
    ) -> SamplingResult:
        """Sample based on parent span decision."""
        return self._sampler.should_sample(parent_context, trace_id, name, kind, attributes, links, trace_state)

    def get_description(self) -> str:
        """Get description of this strategy."""
        return "ParentBasedSampling: Respects parent span sampling decision"


def create_sampling_strategy(ratio: float = 1.0, exclude_endpoints: list[str] | None = None) -> Sampler:
    """Factory function to create a sampling strategy.

    Args:
        ratio: Sampling ratio (0.0 to 1.0)
        exclude_endpoints: List of endpoint patterns to exclude

    Returns:
        Sampler: Configured sampling strategy
    """
    # Start with ratio-based sampling
    base_sampler: Sampler
    if ratio >= 1.0:
        base_sampler = AlwaysSampleStrategy()
    else:
        base_sampler = RatioBasedSamplingStrategy(ratio)

    # Wrap with endpoint exclusion if patterns provided
    if exclude_endpoints:
        base_sampler = EndpointExclusionSamplingStrategy(base_sampler, exclude_endpoints)

    # Wrap with parent-based sampling for distributed tracing
    return ParentBasedSamplingStrategy(base_sampler)
