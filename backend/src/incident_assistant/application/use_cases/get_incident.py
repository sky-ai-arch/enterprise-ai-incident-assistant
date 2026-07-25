from uuid import UUID
from incident_assistant.domain.entities.incident import Incident
from incident_assistant.domain.repositories.incident_repository import (
    IncidentRepository,
)


class GetIncidentUseCase:
    def __init__(self, repository: IncidentRepository):
        self.repository = repository

    def execute(self, incident_id: UUID) -> Incident | None:
        return self.repository.get_by_id(incident_id)