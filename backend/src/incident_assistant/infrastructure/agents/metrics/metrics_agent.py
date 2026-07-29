from incident_assistant.domain.entities.evidence import Evidence
from incident_assistant.domain.interfaces.agent import Agent
from incident_assistant.domain.interfaces.tools.metrics_tools import MetricsTool
from incident_assistant.domain.value_objects.agent_context import AgentContext
from incident_assistant.domain.value_objects.agent_result import AgentResult


class MetricsAgent(Agent):

    def __init__(
        self,
        metrics_tool: MetricsTool,
    ):
        self._metrics_tool = metrics_tool

    @property
    def name(self) -> str:
        return "metrics"

    def execute(
        self,
        context: AgentContext,
    ) -> AgentResult:

        metrics = self._metrics_tool.query(
            "node_cpu_seconds_total"
        )
        sample = metrics.samples[0]
        context.state.evidence.append(
            Evidence(
                source="prometheus",
                evidence_type="metric",
                key="cpu_usage",
                value=sample.value,   # <-- no hardcoded value
                confidence=0.98,
                metadata=sample.labels
            )
        )

        if sample.value > 90:
                    context.state.observations.append(
                        f"CPU utilization is critically high ({sample.value}%)."
                    )

        return AgentResult(
            agent=self.name,
            success=True,
            observations=[
                "Collected CPU metrics.",
            ],
        )