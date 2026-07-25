from incident_assistant.application.schemas.investigation.response import (
    InvestigationResponse,
)
from incident_assistant.domain.value_objects.investigation_result import (
    InvestigationResult,
)


def to_investigation_response(
    result: InvestigationResult,
) -> InvestigationResponse:

    observations: list[str] = []

    for agent_result in result.results:
        observations.extend(agent_result.observations)

    return InvestigationResponse(
        success=result.success,
        observations=observations,
    )