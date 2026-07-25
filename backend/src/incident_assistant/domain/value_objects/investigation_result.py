from __future__ import annotations

from dataclasses import dataclass, field

from incident_assistant.domain.value_objects.agent_result import AgentResult


@dataclass
class InvestigationResult:
    success: bool

    results: list[AgentResult] = field(default_factory=list)