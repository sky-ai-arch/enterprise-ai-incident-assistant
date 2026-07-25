from fastapi import APIRouter, Depends

from incident_assistant.api.dependencies import (
    get_investigation_orchestrator,
)
from incident_assistant.application.mappers.investigation_mapper import (
    to_investigation_response,
)
from incident_assistant.application.orchestrators.investigation_orchestrator import (
    InvestigationOrchestrator,
)
from incident_assistant.application.schemas.investigation.create import (
    CreateInvestigationRequest,
)
from incident_assistant.application.schemas.investigation.response import (
    InvestigationResponse,
)
from incident_assistant.domain.value_objects.agent_context import (
    AgentContext,
)

from uuid import uuid4


router = APIRouter(
    prefix="/investigations",
    tags=["Investigations"],
)

@router.post(
    "",
    response_model=InvestigationResponse,
)
def investigate(
    request: CreateInvestigationRequest,
    orchestrator: InvestigationOrchestrator = Depends(
        get_investigation_orchestrator
    ),
):

    context = AgentContext(
        request_id=uuid4(),
        incident_id=request.incident_id,
        request=request.model_dump(),
    )

    result = orchestrator.execute(context)

    return to_investigation_response(result)