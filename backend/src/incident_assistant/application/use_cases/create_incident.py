from incident_assistant.application.schemas.incident.create import (
    CreateIncidentRequest,
)
from incident_assistant.domain.entities.incident import Incident
from incident_assistant.domain.repositories.incident_repository import (
    IncidentRepository,
)


class CreateIncidentUseCase:

    def __init__(self, repository: IncidentRepository):
        self.repository = repository

    def execute(
        self,
        request: CreateIncidentRequest,
    ) -> Incident:

        incident = Incident(
            title=request.title,
            description=request.description,
            service=request.service,
            created_by=request.created_by,
        )

        return self.repository.create(incident)