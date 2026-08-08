from __future__ import annotations

from incident_assistant.domain.value_objects.hypothesis import (
    Hypothesis,
)
from incident_assistant.domain.value_objects.recommendation import (
    Recommendation,
)


class RecommendationEngine:
    """
    Produces remediation recommendations
    based on generated hypotheses.
    """

    def generate(
        self,
        hypotheses: list[Hypothesis],
    ) -> list[Recommendation]:

        recommendations: list[Recommendation] = []

        for hypothesis in hypotheses:

            if hypothesis.title == "Possible Memory Leak":

                recommendations.append(
                    Recommendation(
                        title="Investigate Memory Usage",
                        description=(
                            "Capture heap dump and analyze "
                            "memory allocations."
                        ),
                        priority="HIGH",
                    )
                )

            elif hypothesis.title == "Deployment Regression":

                recommendations.append(
                    Recommendation(
                        title="Review Latest Deployment",
                        description=(
                            "Inspect the latest deployment "
                            "and consider rollback if required."
                        ),
                        priority="HIGH",
                    )
                )

        return recommendations