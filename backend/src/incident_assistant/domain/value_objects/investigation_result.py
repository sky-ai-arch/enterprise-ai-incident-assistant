from __future__ import annotations

from dataclasses import dataclass, field

from incident_assistant.domain.value_objects.agent_result import AgentResult
from incident_assistant.domain.value_objects.investigation_report import (
    InvestigationReport,
)


@dataclass
class InvestigationResult:

    success: bool

    report: InvestigationReport | None = None

    results: list[AgentResult] = field(
        default_factory=list,
    )