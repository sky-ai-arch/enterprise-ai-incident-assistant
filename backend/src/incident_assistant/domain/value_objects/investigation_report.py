from __future__ import annotations

from dataclasses import dataclass, field

from incident_assistant.domain.value_objects.finding import Finding
from incident_assistant.domain.value_objects.hypothesis import Hypothesis


@dataclass(frozen=True)
class InvestigationReport:
    findings: list[Finding] = field(default_factory=list)
    hypotheses: list[Hypothesis] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    summary: str = ""