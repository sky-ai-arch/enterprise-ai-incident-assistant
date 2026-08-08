from __future__ import annotations

from incident_assistant.domain.value_objects.finding import Finding
from incident_assistant.domain.value_objects.hypothesis import (
    Hypothesis,
)


class HypothesisEngine:
    """
    Generates possible root-cause hypotheses from
    findings and correlated observations.
    """

    def generate(
        self,
        findings: list[Finding],
        correlations: list[str],
    ) -> list[Hypothesis]:

        hypotheses: list[Hypothesis] = []

        titles = {
            finding.title.lower()
            for finding in findings
        }

        if (
            "cpu usage" in titles
            and "error" in titles
        ):

            hypotheses.append(
                Hypothesis(
                    title="Possible Memory Leak",
                    description=(
                        "High CPU utilization together with "
                        "application memory errors suggests "
                        "a possible memory leak."
                    ),
                    confidence=0.90,
                )
            )

        if any(
            "deployment" in text.lower()
            for text in correlations
        ):

            hypotheses.append(
                Hypothesis(
                    title="Deployment Regression",
                    description=(
                        "Recent deployment is likely related "
                        "to the observed system degradation."
                    ),
                    confidence=0.85,
                )
            )

        return hypotheses