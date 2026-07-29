from __future__ import annotations

from abc import ABC, abstractmethod

from incident_assistant.domain.value_objects.log_result import LogEntry


class LogsTool(ABC):

    @abstractmethod
    def query(
        self,
        expression: str,
    ) -> LogEntry:
        raise NotImplementedError