from __future__ import annotations

from incident_assistant.application.graph.investigation_graph import (
    InvestigationGraph,
)
from incident_assistant.application.graph.investigation_state import (
    InvestigationGraphState,
)
from incident_assistant.domain.value_objects.agent_context import (
    AgentContext,
)
from incident_assistant.domain.value_objects.investigation_result import (
    InvestigationResult,
)


class InvestigationOrchestrator:

    def __init__(
        self,
        graph: InvestigationGraph,
    ):
        self._graph = graph

    def execute(
        self,
        context: AgentContext,
    ) -> InvestigationResult:

        state: InvestigationGraphState = {
            "context": context,
            "results": [],
            "report": None,
            "current_round": 0,
            "additional_investigation_required": False,
        }

        final_state = self._graph.execute(
            state
        )

        return InvestigationResult(
            success=True,
            report=final_state["report"],
            results=final_state["results"],
        )