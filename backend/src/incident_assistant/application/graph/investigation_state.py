from __future__ import annotations

from typing import TypedDict

from incident_assistant.domain.value_objects.agent_context import (
    AgentContext,
)
from incident_assistant.domain.value_objects.agent_result import (
    AgentResult,
)
from incident_assistant.domain.value_objects.investigation_report import (
    InvestigationReport,
)


class InvestigationGraphState(TypedDict):

    context: AgentContext

    results: list[AgentResult]

    report: InvestigationReport | None

    current_round: int

    additional_investigation_required: bool