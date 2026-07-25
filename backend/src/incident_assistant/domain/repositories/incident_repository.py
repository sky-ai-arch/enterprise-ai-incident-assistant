from __future__ import annotations
from uuid import UUID
from abc import ABC, abstractmethod

from incident_assistant.domain.entities.incident import Incident


class IncidentRepository(ABC):

    @abstractmethod
    def create(self, incident: Incident) -> Incident:
        ...

    @abstractmethod
    def get_by_id(self, incident_id: UUID) -> Incident | None:
        ...

    @abstractmethod
    def list(self) -> list[Incident]:
        ...

    @abstractmethod
    def delete(self, incident_id: UUID) -> None:
        ...