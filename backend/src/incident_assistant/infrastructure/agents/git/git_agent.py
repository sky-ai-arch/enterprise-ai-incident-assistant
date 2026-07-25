from incident_assistant.domain.interfaces.agent import Agent
from incident_assistant.domain.value_objects.agent_context import (
    AgentContext,
)
from incident_assistant.domain.value_objects.agent_result import AgentResult

class GitAgent(Agent):

    @property
    def name(self) -> str:
        return "git"

    def execute(
            self,
            context: AgentContext,
        ) -> AgentResult:

        context.state.evidence.append(
            Evidence(
                source="github",
                evidence_type="deployment",
                key="last_commit",
                value="9d5bc7f",
                confidence=1.0,
            )
        )

        context.state.observations.append(
            "Recent deployment detected."
        )

        return AgentResult(
            agent=self.name,
            success=True,
            observations=[
                "Collected deployment history."
            ],
        )