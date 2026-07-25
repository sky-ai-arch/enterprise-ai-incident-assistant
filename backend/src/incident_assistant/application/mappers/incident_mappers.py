from incident_assistant.application.schemas.incident.response import (
    IncidentResponse,
)
from incident_assistant.domain.entities.incident import Incident


def to_incident_response(
    incident: Incident,
) -> IncidentResponse:

    return IncidentResponse(
        id=str(incident.id),
        title=incident.title,
        description=incident.description,
        service=incident.service,
        severity=incident.severity.value,
        status=incident.status.value,
        created_by=incident.created_by,
    )