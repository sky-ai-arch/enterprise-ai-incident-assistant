from incident_assistant.domain.interfaces.agent import Agent
from incident_assistant.domain.value_objects.agent_context import (
    AgentContext,
)
from incident_assistant.domain.value_objects.agent_result import AgentResult


class LogsAgent(Agent):

    @property
    def name(self) -> str:
        return "logs"
    def execute(
                self,
                context: AgentContext,
            ) -> AgentResult:

        context.state.evidence.append(
                    Evidence(
                        source="loki",
                        evidence_type="log",
                        key="oom_killed",
                        value=True,
                        confidence=0.95,
                    )
                )

        context.state.observations.append(
            "Detected repeated OOMKilled events."
        )

        return AgentResult(
            agent=self.name,
            success=True,
            observations=[
                "Collected application logs."
            ],
        )