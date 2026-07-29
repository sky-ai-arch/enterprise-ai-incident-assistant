from incident_assistant.application.schemas.investigation.finding import (
    FindingResponse,
)
from incident_assistant.application.schemas.investigation.hypothesis import (
    HypothesisResponse,
)
from incident_assistant.application.schemas.investigation.recommendation import (
    RecommendationResponse,
)
from incident_assistant.application.schemas.investigation.report import (
    InvestigationReportResponse,
)
from incident_assistant.application.schemas.investigation.result import (
    AgentResultResponse,
)
from incident_assistant.application.schemas.investigation.response import (
    InvestigationResponse,
)
from incident_assistant.domain.value_objects.investigation_result import (
    InvestigationResult,
)


def to_investigation_response(
    result: InvestigationResult,
) -> InvestigationResponse:

    report = result.report

    return InvestigationResponse(
        success=result.success,
        report=InvestigationReportResponse(
            summary=report.summary,
            findings=[
                FindingResponse(
                    title=f.title,
                    description=f.description,
                    confidence=f.confidence,
                    evidence_keys=f.evidence_keys,
                )
                for f in report.findings
            ],
            hypotheses=[
                HypothesisResponse(
                    title=h.title,
                    description=h.description,
                    confidence=h.confidence,
                )
                for h in report.hypotheses
            ],
            recommendations=[
                RecommendationResponse(
                    title=r.title,
                    description=r.description,
                    priority=r.priority,
                )
                for r in report.recommendations
            ],
        ),
        results=[
            AgentResultResponse(
                agent=r.agent,
                success=r.success,
                observations=r.observations,
            )
            for r in result.results
        ],
    )