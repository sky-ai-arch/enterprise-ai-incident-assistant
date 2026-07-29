from __future__ import annotations

from pydantic import BaseModel

from incident_assistant.application.schemas.investigation.report import (
    InvestigationReportResponse,
)
from incident_assistant.application.schemas.investigation.result import (
    AgentResultResponse,
)


class InvestigationResponse(BaseModel):

    success: bool

    report: InvestigationReportResponse

    results: list[AgentResultResponse]