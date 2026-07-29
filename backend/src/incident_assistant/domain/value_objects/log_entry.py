from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class LogEntry:

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    
    level: str = "INFO"

    message: str = ""

    labels: dict[str, str] = field(default_factory=dict)