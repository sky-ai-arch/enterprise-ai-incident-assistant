from __future__ import annotations

from incident_assistant.domain.value_objects.agent_context import (
    AgentContext,
)


class InvestigationEdges:

    @staticmethod
    def should_continue(
        context: AgentContext,
    ) -> str:

        if context.metadata.get(
            "additional_investigation_required",
            False,
        ):
            return "continue"

        return "report"