from incident_assistant.domain.interfaces.agent import Agent
from incident_assistant.domain.value_objects.agent_context import AgentContext
from incident_assistant.domain.value_objects.agent_result import AgentResult
from incident_assistant.domain.value_objects.investigation_report import (
    InvestigationReport,
)


class ReporterAgent(Agent):

    @property
    def name(self) -> str:
        return "reporter"

    def execute(
        self,
        context: AgentContext,
        report: InvestigationReport,
    ) -> AgentResult:

        context.state.report = report

        return AgentResult(
            agent=self.name,
            success=True,
            observations=[
                "Investigation report generated."
            ],
            artifacts={
                "report": report,
            },
        )