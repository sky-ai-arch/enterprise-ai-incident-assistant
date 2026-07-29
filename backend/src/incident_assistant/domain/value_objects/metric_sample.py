from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class MetricSample:

    labels: dict[str, str]

    value: Any

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )