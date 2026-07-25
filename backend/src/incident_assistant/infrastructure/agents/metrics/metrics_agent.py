from incident_assistant.domain.entities.evidence import Evidence
from incident_assistant.domain.interfaces.agent import Agent
from incident_assistant.domain.value_objects.agent_context import (
    AgentContext,
)
from incident_assistant.domain.value_objects.agent_result import (
    AgentResult,
)


class MetricsAgent(Agent):

    @property
    def name(self) -> str:
        return "metrics"

    def execute(
        self,
        context: AgentContext,
    ) -> AgentResult:

        context.state.evidence.append(
            Evidence(
                source="prometheus",
                evidence_type="metric",
                key="cpu_usage",
                value="98%",
                confidence=0.98,
                metadata={
                    "namespace": "production",
                    "pod": "api-server-7f98",
                },
            )
        )

        context.state.observations.append(
            "CPU utilization is critically high."
        )

        return AgentResult(
            agent=self.name,
            success=True,
            observations=[
                "Collected CPU metrics.",
            ],
        )