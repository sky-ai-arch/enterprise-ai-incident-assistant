from __future__ import annotations

from abc import ABC, abstractmethod

from incident_assistant.domain.value_objects.metrics_result import MetricResult


class MetricsTool(ABC):

    @abstractmethod
    def query(
        self,
        expression: str,
    ) -> MetricResult:
        """Execute a metrics query."""
        raise NotImplementedError

