from __future__ import annotations

from incident_assistant.domain.entities.evidence import Evidence
from incident_assistant.domain.value_objects.agent_context import AgentContext
from incident_assistant.domain.value_objects.finding import Finding
from incident_assistant.domain.value_objects.hypothesis import Hypothesis
from incident_assistant.domain.value_objects.investigation_report import (
    InvestigationReport,
)


class InvestigationAnalyzer:

    def analyze(
        self,
        context: AgentContext,
    ) -> InvestigationReport:

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

        # Very simple first reasoning rule
        keys = {e.key for e in context.state.evidence}

        if {
            "cpu_usage",
            "latest_error",
            "last_commit",
        }.issubset(keys):

            hypotheses.append(
                Hypothesis(
                    title="Recent deployment may have introduced resource issues",
                    description=(
                        "High CPU usage, application errors, and a recent "
                        "deployment were observed together."
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
                    "Review the most recent deployment.",
                    "Inspect application logs around deployment time.",
                    "Consider rollback if the issue started immediately after deployment.",
                ]
            )

        return InvestigationReport(
            findings=findings,
            hypotheses=hypotheses,
            recommendations=recommendations,
            summary="Initial automated investigation completed.",
        )