from dataclasses import dataclass, field
from typing import Any
from incident_assistant.domain.entities.evidence import Evidence
from incident_assistant.domain.value_objects.investigation_report import (
    InvestigationReport,
)

@dataclass
class InvestigationState:

    evidence: list[Evidence] = field(default_factory=list)

    observations: list[str] = field(default_factory=list)

    artifacts: dict[str, Any] = field(default_factory=dict)

    report: InvestigationReport | None = None