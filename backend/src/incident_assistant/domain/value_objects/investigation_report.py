from __future__ import annotations

from dataclasses import dataclass, field

from incident_assistant.domain.value_objects.finding import Finding
from incident_assistant.domain.value_objects.hypothesis import Hypothesis
from incident_assistant.domain.value_objects.recommendation import Recommendation


@dataclass
class InvestigationReport:

    findings: list[Finding] = field(default_factory=list)

    hypotheses: list[Hypothesis] = field(default_factory=list)

    recommendations: list[Recommendation] = field(
        default_factory=list
    )

    summary: str = ""

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> InvestigationReport:

        return cls(
            findings=[
                Finding(**finding)
                for finding in data.get("findings", [])
            ],
            hypotheses=[
                Hypothesis(**hypothesis)
                for hypothesis in data.get("hypotheses", [])
            ],
            recommendations=[
                Recommendation(**recommendation)
                for recommendation in data.get(
                    "recommendations",
                    [],
                )
            ],
            summary=data.get("summary", ""),
        )