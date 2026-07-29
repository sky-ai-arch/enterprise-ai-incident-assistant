from dataclasses import dataclass, field
from datetime import UTC, datetime

from incident_assistant.domain.value_objects.metric_sample import MetricSample


@dataclass(frozen=True)
class MetricResult:

    query: str

    collected_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    samples: list[MetricSample] = field(default_factory=list)