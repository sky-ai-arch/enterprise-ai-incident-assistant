from incident_assistant.domain.interfaces.agent import Agent
from incident_assistant.domain.value_objects.agent_context import (
    AgentContext,
)
from incident_assistant.domain.value_objects.agent_result import AgentResult
from incident_assistant.domain.entities.evidence import Evidence
from incident_assistant.domain.interfaces.tools.logs_tools import LogsTool


class LogsAgent(Agent):

    @property
    def name(self) -> str:
        return "logs"

    def __init__(
        self,
        logs_tool: LogsTool,
    ):
        self._logs_tool = logs_tool

    def execute(
                self,
                context: AgentContext,
            ) -> AgentResult:
        logs = self._logs_tool.query(
                                '{namespace="production"}'
                            )

        entry = logs.entries[0]
        context.state.evidence.append(
        Evidence(
            source="loki",
            evidence_type="log",
            key="error",
            value=entry.message,
            collected_at=entry.timestamp,
            metadata=entry.labels,
        )
    )

        context.state.observations.append(f"Error log detected: {entry.message}")


        return AgentResult(
            agent=self.name,
            success=True,
            observations=[
                "Collected application logs."
            ],
        )
