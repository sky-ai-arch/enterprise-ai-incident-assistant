from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Hypothesis:
    title: str
    description: str
    confidence: float
    supporting_findings: list[str] = field(default_factory=list)