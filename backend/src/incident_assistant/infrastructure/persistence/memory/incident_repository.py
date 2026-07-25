from uuid import UUID

from incident_assistant.domain.entities.incident import Incident
from incident_assistant.domain.repositories.incident_repository import (
    IncidentRepository,
)


class InMemoryIncidentRepository(IncidentRepository):
    def __init__(self):
        self._storage: dict[UUID, Incident] = {}

    def create(self, incident: Incident) -> Incident:
        self._storage[incident.id] = incident
        return incident

    def get_by_id(self, incident_id: UUID) -> Incident | None:
        return self._storage.get(incident_id)

    def list(self) -> list[Incident]:
        return list(self._storage.values())

    def delete(self, incident_id: UUID) -> None:
        self._storage.pop(incident_id, None)