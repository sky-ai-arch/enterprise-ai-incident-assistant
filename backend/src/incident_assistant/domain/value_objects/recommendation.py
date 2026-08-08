from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Recommendation:

    title: str

    description: str

    priority: str

    evidence_keys: list[str] = field(
        default_factory=list
    )