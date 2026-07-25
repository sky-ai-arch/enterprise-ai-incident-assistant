from incident_assistant.domain.entities.incident import Incident
from incident_assistant.domain.repositories.incident_repository import (
    IncidentRepository,
)


class ListIncidentsUseCase:
    def __init__(self, repository: IncidentRepository):
        self.repository = repository

    def execute(self) -> list[Incident]:
        return self.repository.list()