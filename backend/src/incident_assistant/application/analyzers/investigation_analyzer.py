from __future__ import annotations

from incident_assistant.domain.value_objects.agent_context import (
    AgentContext,
)
from incident_assistant.domain.value_objects.finding import (
    Finding,
)
from incident_assistant.domain.value_objects.hypothesis import (
    Hypothesis,
)
from incident_assistant.domain.value_objects.investigation_report import (
    InvestigationReport,
)


class InvestigationAnalyzer:

    def analyze(
        self,
        context: AgentContext,
    ) -> InvestigationReport:
        print("Analyzer executed")
        findings: list[Finding] = []

        for evidence in context.state.evidence:

            findings.append(
                Finding(
                    title=evidence.key,
                    description=str(evidence.value),
                    confidence=evidence.confidence,
                    evidence_keys=[evidence.key],
                )
            )

        hypotheses: list[Hypothesis] = []

        recommendations: list[str] = []

        keys = {
            evidence.key
            for evidence in context.state.evidence
        }

        if {
            "cpu_usage",
            "latest_error",
            "last_commit",
        }.issubset(keys):

            hypotheses.append(
                Hypothesis(
                    title="Deployment introduced performance issue",
                    description=(
                        "High CPU, application errors and a recent deployment "
                        "were detected together."
                    ),
                    confidence=0.90,
                    supporting_findings=[
                        "cpu_usage",
                        "latest_error",
                        "last_commit",
                    ],
                )
            )

            recommendations.extend(
                [
                    "Inspect the latest deployment.",
                    "Review application logs.",
                    "Rollback if necessary.",
                ]
            )
        print("investigation report is generated")
        return InvestigationReport(
            findings=findings,
            hypotheses=hypotheses,
            recommendations=recommendations,
            summary="Initial automated investigation completed.",
        )