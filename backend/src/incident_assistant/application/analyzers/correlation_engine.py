from __future__ import annotations

from incident_assistant.domain.entities.evidence import Evidence


class CorrelationEngine:
    """
    Correlates evidence collected from different investigation agents.

    This engine does not generate findings or hypotheses.
    It only discovers relationships between evidence.
    """

    def correlate(
        self,
        evidence: list[Evidence],
    ) -> list[str]:

        observations: list[str] = []

        cpu = next(
            (
                item
                for item in evidence
                if item.key == "cpu_usage"
            ),
            None,
        )

        error = next(
            (
                item
                for item in evidence
                if item.key == "error"
            ),
            None,
        )

        deployment = next(
            (
                item
                for item in evidence
                if item.key == "last_commit"
            ),
            None,
        )

        if cpu and error:
            observations.append(
                "High CPU usage correlates with OutOfMemory errors."
            )

        if deployment and error:
            observations.append(
                "Application failures started after the latest deployment."
            )

        if deployment and cpu:
            observations.append(
                "CPU utilization increased after the latest deployment."
            )

        if cpu and deployment and error:
            observations.append(
                "Multiple telemetry sources indicate a deployment-related incident."
            )

        return observations