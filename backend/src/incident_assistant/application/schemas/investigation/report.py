from __future__ import annotations

from pydantic import BaseModel

from incident_assistant.application.schemas.investigation.finding import (
    FindingResponse,
)
from incident_assistant.application.schemas.investigation.hypothesis import (
    HypothesisResponse,
)
from incident_assistant.application.schemas.investigation.recommendation import (
    RecommendationResponse,
)


class InvestigationReportResponse(BaseModel):

    summary: str

    findings: list[FindingResponse]

    hypotheses: list[HypothesisResponse]

    recommendations: list[RecommendationResponse]