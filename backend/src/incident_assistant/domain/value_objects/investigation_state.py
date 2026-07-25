from dataclasses import dataclass, field
from typing import Any
from incident_assistant.domain.entities.evidence import Evidence


@dataclass
class InvestigationState:

    evidence: list[Evidence] = field(default_factory=list)

    observations: list[str] = field(default_factory=list)

    artifacts: dict[str, Any] = field(default_factory=dict)