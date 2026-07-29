from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Finding:
    title: str
    description: str
    confidence: float
    evidence_keys: list[str] = field(default_factory=list)