from __future__ import annotations

from dataclasses import dataclass, field

from incident_assistant.domain.value_objects.log_entry import LogEntry


@dataclass(frozen=True)
class LogResult:
    query: str
    entries: list[LogEntry] = field(default_factory=list)