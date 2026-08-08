from __future__ import annotations

from incident_assistant.domain.entities.evidence import Evidence
from incident_assistant.domain.value_objects.finding import Finding


class FindingEngine:
    """
    Converts raw evidence into investigation findings.
    """

    def generate(
        self,
        evidence: list[Evidence],
    ) -> list[Finding]:

        findings: list[Finding] = []

        for item in evidence:

            findings.append(
                Finding(
                    title=item.key.replace("_", " ").title(),
                    description=str(item.value),
                    confidence=item.confidence,
                    evidence_keys=[
                        item.key,
                    ],
                )
            )

        return findings