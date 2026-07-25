
from incident_assistant.domain.interfaces.agent import Agent
from incident_assistant.domain.value_objects.agent_context import (
    AgentContext,
)
from incident_assistant.domain.value_objects.agent_result import AgentResult

class ReporterAgent(Agent):

    @property
    def name(self) -> str:
        return "reporter"
        
    def execute(
        self,
        context: AgentContext,
    ) -> AgentResult:

        summary = "\n".join(context.state.observations)

        context.state.artifacts["report"] = summary

        return AgentResult(
            agent=self.name,
            success=True,
            observations=[
                "Generated investigation report."
            ],
            artifacts={
                "report": summary,
            },
        )