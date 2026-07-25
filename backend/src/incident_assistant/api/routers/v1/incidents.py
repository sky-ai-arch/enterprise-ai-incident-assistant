from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from incident_assistant.api.dependencies import get_incident_repository
from incident_assistant.application.schemas.incident.create import (
    CreateIncidentRequest,
)
from incident_assistant.application.mappers.incident_mappers import (
    to_incident_response,
)


from incident_assistant.application.schemas.incident.response import (
    IncidentResponse,
)
from incident_assistant.application.use_cases.create_incident import (
    CreateIncidentUseCase,
)
from incident_assistant.application.use_cases.get_incident import (
    GetIncidentUseCase,
)
from incident_assistant.application.use_cases.list_incidents import (
    ListIncidentsUseCase,
)
from incident_assistant.domain.repositories.incident_repository import (
    IncidentRepository,
)

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.post("", response_model=IncidentResponse)
def create_incident(
    request: CreateIncidentRequest,
    repository: IncidentRepository = Depends(get_incident_repository),
):
    incident = CreateIncidentUseCase(repository).execute(request)

    return to_incident_response(incident)


@router.get("", response_model=list[IncidentResponse])
def list_incidents(
    repository: IncidentRepository = Depends(get_incident_repository),
):
    incidents = ListIncidentsUseCase(repository).execute()

    return [
        to_incident_response(incident)
        for incident in incidents
    ]



@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: UUID,
    repository: IncidentRepository = Depends(get_incident_repository),
):
    incident = GetIncidentUseCase(repository).execute(incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return to_incident_response(incident)